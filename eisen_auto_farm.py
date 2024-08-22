import requests
from stations import Station
import drive_to


def farm():
    api_url = "http://192.168.100.19:2012/hold"
    response = requests.get(api_url)
    request_json = response.json()
    print(request_json)
    if request_json["hold"]["hold_free"] > 0:
        drive_to.set_target(Station.VESTA_STATION.value.get("x"), Station.VESTA_STATION.value.get("y"))
