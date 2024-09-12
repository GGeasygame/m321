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


def setup_keycloak():
    try:
        data = {"client_secret": "79kdqCGiq6aocxVcP3oiGhDTUFU3nu5W",
                "authorize_url": "http://192.168.100.19:8080/realms/master/protocol/openid-connect/auth",
                "token_url": "http://192.168.100.19:8080/realms/master/protocol/openid-connect/token"}

        response = requests.post("http://192.168.100.19:2018/configure_oauth", json=data)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


print(setup_keycloak())

