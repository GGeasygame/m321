import time

import drive_to
import scanner
import interfaces.navigation as navigation
import math
import interfaces.laser as laser
import interfaces.cargo_hold
import asyncio
import threading


def calculate_angle(pos_self, pos_meteroid):
    x = pos_self["x"] - pos_meteroid['x']
    y = pos_self["y"] - pos_meteroid['y']
    print(f"x: {x}, y: {y}")
    if x == 0 and y == 0:
        return 0
    angle = math.degrees(math.atan2(x, y)) - pos_self['angle']
    angle = (angle + 360) % 360  # Normalize angle to [0, 360)
    print(f"Calculated angle: {angle}")
    return angle


class Miner:
    cargo = interfaces.cargo_hold.CargoHoldAPI("http://192.168.100.19:2012")

    def __init__(self, name):
        self.name = name
        self.meteroid = None

    def mine(self):
        scanner.scan(self.mine_with_name)

    def mine_with_name(self, json):
        # Scanning for the meteoroid with the correct name
        self.meteroid = None
        for entry in json:
            if entry['name'] == self.name:
                self.meteroid = entry
                break

        if self.meteroid is None:
            print(f"Meteoroid {self.name} not found.")
            return

        position_self = navigation.get_position()
        position_meteroid = self.meteroid['pos']

        # Set laser angle and start mining
        angle_to_meteroid = calculate_angle(position_self, position_meteroid)
        laser.set_angle(angle_to_meteroid)
        laser.activate()

        print("Laser state:", laser.get_state())

        hold = self.cargo.get_cargo_hold_status()['hold']
        if hold['hold_free'] == 0:
            print("Cargo hold full.")
            return

        if hold['hold_free'] % 12 == 0:
            # Swapping cargo slots if necessary
            asyncio.run_coroutine_threadsafe(self.cargo.swap_to_lowest_available(), loop)

        time.sleep(7)  # Simulate mining time

    async def follow_meteoroid(self):
        while True:
            if self.meteroid:
                position_meteroid = self.meteroid['pos']
                print(f"Driving to meteroid at coordinates: {position_meteroid['x']}, {position_meteroid['y']}")

                # Use the `drive_to` function to move directly towards the meteoroid
                drive_to.set_target(position_meteroid['x'], position_meteroid['y'])

                await asyncio.sleep(1)  # Check again in 1 second

# Function to start the event loop in a background thread
def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Initialize a new event loop for async operations
loop = asyncio.new_event_loop()
t = threading.Thread(target=start_background_loop, args=(loop,), daemon=True)
t.start()

# Main program
miner = Miner("Arakrock 2")

# Start mining and following the meteoroid in parallel
asyncio.run_coroutine_threadsafe(miner.follow_meteoroid(), loop)

while True:
    miner.mine()  # Start the mining process
