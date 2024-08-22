import resource
import navigation
from stations import Station
import drive_to
import interfaces.cargo_hold


class AutoFarm:

    cargo = interfaces.cargo_hold.CargoHoldAPI("http://192.168.100.19:2012")

    def farm(self):
        while True:
            request_json = self.cargo.get_cargo_hold_status()
            self.cargo.display_status()
            if request_json["hold"]["hold_free"] > 0:
                drive_to.set_target(Station.VESTA_STATION.value.get("x"), Station.VESTA_STATION.value.get("y"))
                navigation.monitor_position(Station.VESTA_STATION.value.get("x"), Station.VESTA_STATION.value.get("y"),
                                            self.buy_iron)
                drive_to.set_target(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"))
                navigation.monitor_position(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"),
                                            self.sell_iron)

    def buy_iron(self):
        request_json = self.cargo.get_cargo_hold_status()
        resource.buy(Station.VESTA_STATION.value.get("name"), "IRON", request_json["hold"]["hold_free"])

    def sell_iron(self):
        request_json = self.cargo.get_cargo_hold_status()
        self.cargo.display_status()
        resource.sell(Station.CORE_STATION.value.get("name"), "IRON", request_json["hold"]["resources"]["IRON"])
        self.cargo.get_cargo_hold_status()
        self.cargo.display_status()
