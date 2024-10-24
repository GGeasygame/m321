import follow_station
import drive_to


def chase():
    drive_to.set_target(36764, 22813)
    follow_station.FollowStation().follow_station("Xyron Vex")


chase()
