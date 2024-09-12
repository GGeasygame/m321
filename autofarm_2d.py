import interfaces.navigation as navigation
import interfaces.resource as resource
from stations import Station
import drive_to
import interfaces.cargo_hold
import mine_meteroid


class AutoFarm:
    cargo = interfaces.cargo_hold.CargoHoldAPI("http://192.168.100.19:2012")
    miner = mine_meteroid.Miner(Station.GOLD_STONE.value.get("name"))

    def farm_iron(self):
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
            else:
                drive_to.set_target(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"))
                navigation.monitor_position(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"),
                                            self.sell_iron)

    def buy_iron(self):
        request_json = self.cargo.get_cargo_hold_status()
        while request_json["hold"]["hold_free"] > 0:
            resource.buy(Station.VESTA_STATION.value.get("name"), "IRON", request_json["hold"]["hold_free"])
            if not self.cargo.swap_to_lowest_available():
                break

    def sell_iron(self):
        request_json = self.cargo.get_cargo_hold_status()
        self.cargo.display_status()
        resource.sell(Station.CORE_STATION.value.get("name"), "IRON", request_json["hold"]["resources"]["IRON"])
        self.cargo.get_cargo_hold_status()
        self.cargo.display_status()

    def farm_gold(self):
        while True:
            request_json = self.cargo.get_cargo_hold_status()
            self.cargo.display_status()

            if request_json["hold"]["hold_free"] > 0:
                drive_to.set_target(Station.GOLD_STONE.value.get("x"), Station.GOLD_STONE.value.get("y"))
                navigation.monitor_position(Station.GOLD_STONE.value.get("x"), Station.GOLD_STONE.value.get("y"),
                                            self.miner.mine)
                drive_to.set_target(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"))
                navigation.monitor_position(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"),
                                            self.sell_stone_and_gold)
            else:
                drive_to.set_target(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"))
                navigation.monitor_position(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"),
                                            self.sell_stone_and_gold)

    def sell_stone_and_gold(self):
        request_json = self.cargo.get_cargo_hold_status()
        self.cargo.display_status()
        resource.sell(Station.CORE_STATION.value.get("name"), "STONE", request_json["hold"]["resources"]["STONE"])
        resource.sell(Station.CORE_STATION.value.get("name"), "GOLD", request_json["hold"]["resources"]["GOLD"])
        self.cargo.get_cargo_hold_status()
        self.cargo.display_status()