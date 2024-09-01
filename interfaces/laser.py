import requests


def activate():
    url = "http://192.168.100.19:2018/activate"

    response = requests.post(url)

    print(response.json())


def set_angle(angle):
    url = "http://192.168.100.19:2018/angle"

    data = {
        "angle": angle
    }
    response = requests.put(url, json=data)

    print(response.json())


def get_state():
    url = "http://192.168.100.19:2018/state"

    response = requests.get(url)

    print(response.json())
