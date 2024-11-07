import requests
from pynput import keyboard
import interfaces.energy_management as energy
import time


def send_rest_call(action, key_char):
    urls = {
        'a': "http://192.168.100.19:2006/thruster",
        's': "http://192.168.100.19:2004/thruster",
        'd': "http://192.168.100.19:2005/thruster",
        'w': "http://192.168.100.19:2003/thruster"
    }
    url = urls.get(key_char)
    if not url:
        return  # Exit if key is not mapped

    data = {"thrust_percent": 100 if action == "pressed" else 0}
    try:
        if key_char == 'a':
            requests.put("http://192.168.100.19:2007/thruster", json=data)
        if key_char == 'd':
            requests.put("http://192.168.100.19:2008/thruster", json=data)
        response = requests.put(url, json=data)
        print(f"Sent {action} call for {key_char}. Status: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending {action} call for {key_char}: {e}")


def on_press(key):
    try:
        if key.char in ['a', 's', 'd', 'w']:
            print(f"Key {key.char} pressed")
            send_rest_call("pressed", key.char)
        send_rest_call("released", 's')
    except AttributeError:
        pass  # Skip if key.char is None


def on_release(key):
    try:
        if key.char in ['a', 's', 'd', 'w']:
            print(f"Key {key.char} released")
            send_rest_call("released", key.char)
    except AttributeError:
        pass  # Skip if key.char is None

    if key == keyboard.Key.esc:
        print("ESC pressed. Exiting.")
        return False  # Stop listener if Esc is pressed


energy.set_limits({
        "scanner": 0,
        "thruster_back": 1,
        "thruster_front": 1,
        "thruster_bottom_left": 1,
        "thruster_front_right": 1,
        "thruster_bottom_right": 1,
        "thruster_front_left": 1,
        "laser": 0,
        "jumpdrive": 0,
        "sensor_void_energy": 0,
        "shield_generator": 0,
        "sensor_atomic_field": 0,
        "matter_stabilizer": 0,
        "cargo_bot": 0
    })

# Start the listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()
