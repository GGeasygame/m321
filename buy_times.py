import requests


def buy_item(station, item):
    # URL der API
    url = "http://192.168.100.19:2011/buy_item"

    # Daten, die gesendet werden sollen
    data = {
        "station": station,
        "what": item
    }

    # POST-Anfrage senden
    response = requests.post(url, json=data)

    # Antwort der API ausgeben
    print(response.json())
