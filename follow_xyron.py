import follow_station
import drive_to


def chase():
    drive_to.set_target(-96217, 84174)
    follow_station.FollowStation().follow_station("Xyron Vex")


chase()
