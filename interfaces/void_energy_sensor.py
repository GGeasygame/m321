import requests
import time


def get_measurement():
    id = "1"
    trigger_measurement(id)
    while True:
        response = get_current_status(id)
        if response['state'] == "measured":
            return response['result']
        time.sleep(2)


def trigger_measurement(id):
    response = requests.post('http://192.168.100.19:2037/trigger_measurement', data={"request_id": id})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to trigger measurement. Status code: {response.status_code}")
        return None


def delete_measurement(id):
    response = requests.delete(f"http://192.168.100.19:2037/measurements/{id}")
    if response.status_code != 200:
        print(f"Failed to delete measurement. Status code: {response.status_code}")


def get_current_status(id):
    response = requests.get(f'http://192.168.100.19:2037/measurements/{id}')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get status. Status code: {response.status_code}")
        return None


print(get_measurement())
