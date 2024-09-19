import requests

def get_thruster_back_status():
    url = 'http://192.168.100.19:2003/thruster'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.RequestException as e:
        print(f"Error fetching thruster status: {e}")
        return None

def get_thruster_bottom_left_status():
    url = 'http://192.168.100.19:2007/thruster'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.RequestException as e:
        print(f"Error fetching thruster status: {e}")
        return None

def get_thruster_bottom_right_status():
    url = 'http://192.168.100.19:2008/thruster'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.RequestException as e:
        print(f"Error fetching thruster status: {e}")
        return None

def get_thruster_front_status():
    url = 'http://192.168.100.19:2004/thruster'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.RequestException as e:
        print(f"Error fetching thruster status: {e}")
        return None

def get_thruster_front_left_status():
    url = 'http://192.168.100.19:2005/thruster'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.RequestException as e:
        print(f"Error fetching thruster status: {e}")
        return None

def get_thruster_front_right_status():
    url = 'http://192.168.100.19:2006/thruster'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.RequestException as e:
        print(f"Error fetching thruster status: {e}")
        return None


def check_all_thrusters_zero():
    thruster_status_methods = [
        get_thruster_back_status,
        get_thruster_bottom_left_status,
        get_thruster_bottom_right_status,
        get_thruster_front_status,
        get_thruster_front_left_status,
        get_thruster_front_right_status
    ]

    all_zero = True

    for method in thruster_status_methods:
        status = method()  # Rufe die Methode auf
        if status is not None and status.get('thrust_percent') != 0:
            all_zero = False

    return all_zero
