import interfaces.energy_management as energy
import interfaces.cargo_hold as cargo


def print_hi(name):
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    energy.set_limits({
        "scanner": 0,
        "thruster_back": 1,
        "thruster_front": 1,
        "thruster_bottom_left": 1,
        "thruster_front_right": 1,
        "thruster_bottom_right": 1,
        "thruster_front_left": 1,
        "laser": 0,
        "jumpdrive": 0,
        "sensor_void_energy": 0,
        "shield_generator": 0,
        "sensor_atomic_field": 0,
        "matter_stabilizer": 0,
        "cargo_bot": 1,
    })

    cargo.CargoHoldAPI("http://192.168.100.19:2012").swap_adjacent(11, 1, 11, 2)

    