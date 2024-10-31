import requests
import interfaces.navigation as navigation


def set_target(x, y):
    api_url = "http://192.168.100.19:2009/set_target"
    data = {
        "target": {
            "x": x,
            "y": y
        }
    }

    # Send the POST request with JSON data
    response = requests.post(api_url, json=data)

    # Check the response status code
    if response.status_code == 200:
        print("Target set successfully.")
        print("Response:", response.json())
    else:
        print(f"Failed to set target. Status code: {response.status_code}")
        print("Response:", response.text)


def drive(target_x, target_y):
    own_position = navigation.get_position()
    print(f"target x: {target_x} target y: {target_y} own x: {own_position['x']} own y: {own_position['y']}")
    if own_position['x'] > target_x:
        requests.post("http://192.168.100.19:2007/thruster", json={"thrust_percent": 100})
        requests.post("http://192.168.100.19:2005/thruster", json={"thrust_percent": 100})

    if own_position['x'] < target_x:
        requests.post("http://192.168.100.19:2008/thruster", json={"thrust_percent": 100})
        requests.post("http://192.168.100.19:2006/thruster", json={"thrust_percent": 100})

    if own_position['y'] > target_y:
        requests.post("http://192.168.100.19:2003/thruster", json={"thrust_percent": 100})

    if own_position['y'] < target_y:
        requests.post("http://192.168.100.19:2004/thruster", json={"thrust_percent": 100})


