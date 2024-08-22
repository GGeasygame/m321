import requests


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