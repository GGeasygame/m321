import follow_station
import drive_to


def chase():
    drive_to.set_target(83057, 11601)
    drive_to.drive(83057, 11601)


chase()
