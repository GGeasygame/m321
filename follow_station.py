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
        print(json)
        if 'station' in json:
            for station in json:
                if station['name'] == self.station:
                    drive_to.set_target(station['pos']['x'], station['pos']['y'])
                    time.sleep(1)
