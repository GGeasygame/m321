import time

import requests


def get_position():
    api_url = "http://192.168.100.19:2010/pos"

    # Send the GET request
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Ensure the response contains the necessary fields
        if "pos" in data and "x" in data["pos"] and "y" in data["pos"]:
            x = data["pos"]["x"]
            y = data["pos"]["y"]
            print(f"Position - x: {x}, y: {y}")
            return {x, y}
        else:
            print("The response does not contain 'pos' or 'x' and 'y' coordinates.")
    else:
        print(f"Failed to get position. Status code: {response.status_code}")
        print("Response:", response.text)


def target_reached_action():
    print("Target position reached! Executing action...")


def monitor_position(target_x, target_y, function):
    while True:
        x, y = get_position()

        # Check if the current position matches the target position
        if x is not None and y is not None and is_in_proximity(x, target_x) and is_in_proximity(y, target_y):
            print(is_in_proximity(x, target_x))
            function()
            break  # Exit the loop once the target is reached

        # Wait for 5 seconds before checking again
        time.sleep(5)


def is_in_proximity(pos1, pos2):
    print(pos1, pos2)
    if 30 > pos1 - pos2 > -30:
        return True
    return False
