import requests


def buy_resource(station, resource, amount):
    url = "http://192.168.100.19:2011/buy"

    data = {
        "station": station,
        "what": resource,
        "amount": amount
    }

    response = requests.post(url, json=data)

    print(response.json())
