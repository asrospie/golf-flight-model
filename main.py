import math
from vector import Vector

def deg_to_rad(deg: float) -> float:
    return deg * math.pi / 180

# constants

# m/s
INITIAL_BALL_SPEED = 85.0

# radians/s
INITIAL_BACK_SPIN = 183.26
INITIAL_RIFLE_SPIN = 0.0
INIITAL_SIDE_SPIN = 0.0

# meters
GOLF_BALL_RADIUS = 0.02135
GOLF_BALL_DIAMETER = 2 * GOLF_BALL_RADIUS

# kilograms
GOLF_BALL_MASS = 0.04593

# radians
LAUNCH_ANGLE = deg_to_rad(13.2)
AZIUMUTH = deg_to_rad(0)

# kg/m^3
AIR_DENSITY = 1.225

AREA = math.pi * (GOLF_BALL_RADIUS ** 2)

# meters/second/second
GRAVITY = 9.8

# coefficients
# [0, 0.5]
C_L = 0.1
C_D = 0.1
# [0, 0.02]
C_M = 0.01

YARDS_PER_METER = 1.09361

# HELPER FUNCTIONS
def spin_ratio(v: Vector, w: Vector) -> float:
    s = GOLF_BALL_RADIUS * w.length() / v.length()
    print(f'SPIN RATIO: {s}')
    return s

# 0.1304, 0.9287,-0.8259, 0.0504, 1.2031, -1.1490, 0.01
A = 0.1304
B = 0.9287
C = -0.8259
D = 0.0504 
E = 1.2031
F = -1.1490
G = 0.01
def lift_coefficicent(v: Vector, w: Vector) -> float: 
    s = spin_ratio(v, w)
    return A + B * s + C * (s ** 2)

def drag_coefficient(v: Vector, w: Vector) -> float:
    s = spin_ratio(v, w)
    return D + E * s + F * (s ** 2)

def m_coefficient(v: Vector, w: Vector) -> float:
    s = spin_ratio(v, w)
    return G * s

def q_dynamic_air_pressure(v: Vector) -> float:
    return 0.5 * AIR_DENSITY * v.length_squared()

def force_lift(v: Vector, w: Vector) -> Vector:
    v_x_w = v.cross_product(w)
    c_l = lift_coefficicent(v, w)
    q = q_dynamic_air_pressure(v)
    return c_l * q * AREA * (v_x_w / (v_x_w.length()))

def force_drag(v: Vector, w: Vector) -> Vector:
    return -drag_coefficient(v, w) * q_dynamic_air_pressure(v) * AREA * (v / v.length())

def force_torque(v: Vector, w: Vector) -> Vector:
    return -m_coefficient(v, w) * q_dynamic_air_pressure(v) * GOLF_BALL_DIAMETER * AREA * (w / w.length())

def force_gravity(v: Vector) -> Vector:
    k = v / v.length()
    k_hat = k.z
    return Vector(0, 0, -GOLF_BALL_MASS * GRAVITY * k_hat)

def apply_force(v: Vector, w: Vector) -> Vector:
    f_l = force_lift(v, w)
    f_d = force_drag(v, w)
    f_g = force_gravity(v)
    print(f'\t\tApply Force: Lift: {f_l.x:.2f} {f_l.y:.2f} {f_l.z:.2f}')
    print(f'\t\tApply Force: Drag: {f_d.x:.2f} {f_d.y:.2f} {f_d.z:.2f}')
    print(f'\t\tApply Force: Gravity: {f_g.x:.2f} {f_g.y:.2f} {f_g.z:.2f}')
    f = f_l + f_d + f_g
    print(f'\t\tApply Force: Total: {f.x:.2f} {f.y:.2f} {f.z:.2f}')
    return f

def mass_moment_of_inertia() -> float:
    return (2 / 5) * GOLF_BALL_MASS * (GOLF_BALL_RADIUS ** 2)
# END HELPER FUNCTIONS

def initial_velocity() -> Vector:
    return Vector(
        INITIAL_BALL_SPEED * math.cos(LAUNCH_ANGLE) * math.sin(AZIUMUTH), 
        INITIAL_BALL_SPEED * math.cos(LAUNCH_ANGLE) * math.cos(AZIUMUTH), 
        INITIAL_BALL_SPEED * math.sin(LAUNCH_ANGLE)
    )

def step(v: Vector, w: Vector, r: Vector, dt: float):
    d_v = apply_force(v, w) / GOLF_BALL_MASS
    d_w = -1 * force_torque(v, w) / mass_moment_of_inertia()
    d_r = v 
    print(f'\t\tDelta: {dt}')
    print(f'\t\tStep: Velocity: {d_v.x:.2f} {d_v.y:.2f} {d_v.z:.2f}')
    print(f'\t\tStep: Rotation: {d_w.x:.2f} {d_w.y:.2f} {d_w.z:.2f}')
    print(f'\t\tStep: Position: {d_r.x:.2f} {d_r.y:.2f} {d_r.z:.2f}')
    d_v *= dt
    d_w *= dt
    d_r *= dt
    d_v += v
    d_w += w
    d_r += r
    return d_v, d_w, d_r

def simulate():
    initial_position = Vector(0.0, 0.0, 0.0)
    velocity: Vector = initial_velocity() 
    rotation: Vector = Vector(INITIAL_BACK_SPIN, INITIAL_RIFLE_SPIN, INIITAL_SIDE_SPIN) 
    position: Vector = initial_position 
    delta: float = 0.1
    print(f'Initial Data')
    print(f'0\tVelocity:\t{velocity.x:.2f} {velocity.y:.2f} {velocity.z:.2f}')
    print(f'0\tRotation:\t{rotation.x:.2f} {rotation.y:.2f} {rotation.z:.2f}')
    print(f'0\tPosition:\t{position.x:.2f} {position.y:.2f} {position.z:.2f}')

    total_time: float = 0.0
    for i in range(1000):
        print('============================================================')
        print(f'{i + 1}\tStart Velocity:\t{velocity.x:.2f} {velocity.y:.2f} {velocity.z:.2f}')
        print(f'{i + 1}\tStart Rotation:\t{rotation.x:.2f} {rotation.y:.2f} {rotation.z:.2f}')
        print(f'{i + 1}\tStart Position:\t{position.x:.2f} {position.y:.2f} {position.z:.2f}')
        total_time += delta
        velocity, rotation, position = step(velocity, rotation, position, delta)

        # print position
        print(f'{i + 1}\tEnd Velocity:\t{velocity.x:.2f} {velocity.y:.2f} {velocity.z:.2f}')
        print(f'{i + 1}\tEnd Rotation:\t{rotation.x:.2f} {rotation.y:.2f} {rotation.z:.2f}')
        print(f'{i + 1}\tEnd Position:\t{position.x:.2f} {position.y:.2f} {position.z:.2f}')
        print(f'{i + 1}\tDistance Travelled: {position.distance_to(initial_position) * YARDS_PER_METER:.2f}')

        if position.z <= 0:
            break
    
    print('============================================================')
    print(f'Total Time: {total_time:.2f}s')

def main():
    simulate()

if __name__ == "__main__":
    main()