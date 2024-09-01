import time

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
    if x < 0 and y < 0:
        angle = math.fabs(math.degrees(math.atan(x / y))) + 360 - pos_self['angle']
        print(f"angle: {angle}")
        return angle
    if x < 0 and y > 0:
        angle = 360 - pos_self['angle'] + 180 - math.fabs(math.degrees(math.atan(x / y)))
        print(f"angle: {angle}")
        return angle
    if x > 0 and y > 0:
        angle = math.fabs(math.degrees(math.atan(x / y))) + 360 - pos_self['angle'] + 180
        print(f"angle: {angle}")
        return angle
    if x > 0 and y < 0:
        angle = + 360 - pos_self['angle'] - math.fabs(math.degrees(math.atan(x / y)))
        print(f"angle: {angle}")
        return angle


class Miner:
    cargo = interfaces.cargo_hold.CargoHoldAPI("http://192.168.100.19:2012")

    def __init__(self, name):
        self.name = name

    def mine(self):
        scanner.scan(self.mine_with_name)

    def mine_with_name(self, json):
        meteroid = None
        for entry in json:
            if entry['name'] == self.name:
                meteroid = entry
        position_self = navigation.get_position()
        position_meteroid = meteroid['pos']
        laser.set_angle(calculate_angle(position_self, position_meteroid))
        laser.activate()
        print(laser.get_state())
        hold = self.cargo.get_cargo_hold_status()['hold']
        if hold['hold_free'] == 0:
            return
        if hold['hold_free'] % 12 == 0:
            asyncio.run_coroutine_threadsafe(self.cargo.swap_to_lowest_available(), loop)

        time.sleep(7)


# Function to start the event loop in a background thread
def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


# Initialize a new event loop
loop = asyncio.new_event_loop()
t = threading.Thread(target=start_background_loop, args=(loop,), daemon=True)
t.start()
