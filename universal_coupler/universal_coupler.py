from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PERMASTORE_URL = 'http://192.168.100.19:2019'


@app.route('/<station_name>/receive', methods=['POST'])
def receive_data(station_name):
    # Request to Permastore to download data
    response = requests.post(
        f'{PERMASTORE_URL}/download',
        json={'source': station_name, 'destination': station_name}
    )

    # Check response from Permastore
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"status": "Error retrieving data"}), 500


@app.route('/<station_name>/send', methods=['POST'])
def send_data(station_name):
    # Extract data from the request
    data = request.get_json()

    # Validate data
    if not data or 'source' not in data or 'data' not in data:
        return jsonify({"status": "Invalid request data"}), 400

    # Send data to Permastore
    response = requests.post(
        f'{PERMASTORE_URL}/upload',
        json={'source': data['source'], 'destination': station_name}
    )

    # Check response from Permastore
    if response.status_code == 200:
        return jsonify({"status": "Data saved"}), 200
    else:
        return jsonify({"status": "Error saving data"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023)
