import requests
import resource
import navigation
from stations import Station
import drive_to


request_json = dict()


def farm():
    api_url = "http://192.168.100.19:2012/hold"
    response = requests.get(api_url)
    request_json = response.json()
    print(request_json)
    if request_json["hold"]["hold_free"] > 0:
        drive_to.set_target(Station.VESTA_STATION.value.get("x"), Station.VESTA_STATION.value.get("y"))
        navigation.monitor_position(Station.VESTA_STATION.value.get("x"), Station.VESTA_STATION.value.get("y"), buy_iron)
        drive_to.set_target(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"))
        navigation.monitor_position(Station.CORE_STATION.value.get("x"), Station.CORE_STATION.value.get("y"), sell_iron)


def buy_iron():
    resource.buy(Station.VESTA_STATION.value.get("name"), "iron", request_json["hold"]["hold_free"])


def sell_iron():
    resource.sell(Station.CORE_STATION.value.get("name"), "iron", request_json["resources"]["iron"])
