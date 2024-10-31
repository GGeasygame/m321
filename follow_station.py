import time

import scanner
import drive_to


class FollowStation:
    def __init__(self):
        self.station = None

    def follow_station(self, station):
        self.station = station
        scanner.scan(self.follow)

    def follow(self, json):
        for station in json:
            if station['name'] == self.station:
                print(f"following {self.station} with position x: {station['pos']['x']} y: {station['pos']['y']}")
                drive_to.drive(station['pos']['x'], station['pos']['y'])
                time.sleep(2)
