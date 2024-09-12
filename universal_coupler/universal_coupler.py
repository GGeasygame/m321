from flask import Flask, request, jsonify
import requests
import xmlrpc.client
import json
from typing import List, Tuple
import base64

app = Flask(__name__)

PERMASTORE_URL = 'http://192.168.100.19:2019'

ZURRO_STATION = {"x": 5608, "y": 9386, "name": "Zurro Station"}
VESTA_STATION = {"x": 10000, "y": 10000, "name": "Vesta Station"}
CORE_STATION = {"x": 0, "y": 0, "name": "Core Station"}
AZURA_STATION = {"x": -1000, "y": 1000, "name": "Azura Station"}
STATION_19_A = {"x": -15526, "y": -12527, "name": "Station 19-A"}
SHANGRIS_STATION = {"x": 4143, "y": 4808, "name": "Shangris Station"}
GOLD_STONE = {"x": -9800, "y": 20200, "name": "Gold Stone"}
ARTEMIS_STATION = {"x": -20000, "y": 38000, "name": "Artemis Station"}


@app.route('/<station_name>/receive', methods=['POST'])
def receive_data(station_name):
    if station_name == ARTEMIS_STATION.get('name'):
        url = 'http://192.168.100.19:2024/RPC2'
        client = xmlrpc.client.ServerProxy(url)
        try:
            data = client.receive()

            return jsonify(convert_to_json_format(data))
        except Exception as e:
            return jsonify({"status": "Error retrieving data", "message": str(e)}), 500
    return jsonify({"status": "Error", "message": "Station not found"}), 404


@app.route('/<station_name>/send', methods=['POST'])
def send_data(station_name):
    # Extract data from the request
    data = request.get_json()

    if not data or 'source' not in data or 'data' not in data:
        return jsonify({"status": "Invalid request data"}), 400

    if station_name == AZURA_STATION.get("name"):
        base64_data = base64.b64encode(data['data'].encode('utf-8')).decode('utf-8')
        payload = {
            "sending_station": data['source'],
            "base64data": base64_data
        }
        try:
            response = requests.post("http://192.168.100.19:2030/put_message", json=payload)
            if response.status_code == 200:
                return jsonify({"status": "Data sent successfully"}), 200
            else:
                return jsonify({"status": "Error sending data", "message": response.text}), 500
        except requests.RequestException as e:
            return jsonify({"status": "Error sending data", "message": str(e)}), 500

    return jsonify({"status": "Error", "message": "Station not found"}), 404


from typing import List, Tuple, Union


def convert_to_json_format(data: Union[List[Tuple[str, bytearray]], Tuple[str, bytearray]]) -> dict:
    messages = []

    # Check if data is a single tuple or a list of tuples
    if isinstance(data, tuple):
        data = [data]  # Convert single tuple to a list of one tuple

    for destination, byte_data in data:
        # Convert ByteArray to a list of integers
        byte_list = list(byte_data)
        messages.append({
            "destination": destination,
            "data": byte_list
        })

    result = {
        "kind": "success",
        "messages": messages
    }

    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023)
