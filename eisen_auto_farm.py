import requests
import resource
import navigation
from stations import Station
import drive_to


class AutoFarm:
    request_json = dict()

    def farm(self):
        api_url = "http://192.168.100.19:2012/hold"
        response = requests.get(api_url)
        self.request_json = response.json()
        print(self.request_json)
        if self.request_json["hold"]["hold_free"] > 0:
            drive_to.set_target(Station.VESTA_STATION.value.get("x"), Station.VESTA_STATION.value.get("y"))
            navigation.monitor_position(Station.VESTA_STATION.value.get("x"), Station.VESTA_STATION.value.get("y"),
                                        self.buy_iron)
            drive_to.set_target(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"))
            navigation.monitor_position(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"),
                                        self.sell_iron)

    def buy_iron(self):
        resource.buy(Station.VESTA_STATION.value.get("name"), "IRON", self.request_json["hold"]["hold_free"])

    def sell_iron(self):
        print(self.request_json)
        resource.sell(Station.CORE_STATION.value.get("name"), "IRON", self.request_json["hold"]["resources"]["IRON"])
