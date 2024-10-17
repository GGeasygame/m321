from flask import Flask, request, jsonify
import requests
import xmlrpc.client
import json
from xmlrpc.client import Binary
import base64
import websockets
from quart import Quart, request, jsonify
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Quart(__name__)

PERMASTORE_URL = 'http://192.168.100.19:2019'

ZURRO_STATION = {"x": 5608, "y": 9386, "name": "Zurro Station"}
VESTA_STATION = {"x": 10000, "y": 10000, "name": "Vesta Station"}
CORE_STATION = {"x": 0, "y": 0, "name": "Core Station"}
AZURA_STATION = {"x": -1000, "y": 1000, "name": "Azura Station"}
STATION_19_A = {"x": -15526, "y": -12527, "name": "Station 19-A"}
SHANGRIS_STATION = {"x": 4143, "y": 4808, "name": "Shangris Station"}
GOLD_STONE = {"x": -9800, "y": 20200, "name": "Gold Stone"}
ARTEMIS_STATION = {"x": -20000, "y": 38000, "name": "Artemis Station"}
ELYSE_TERMINAL = {"x": 72701, "y": -78179, "name": "Elyse Terminal"}


@app.route('/<station_name>/receive', methods=['POST'])
async def receive_data(station_name):
    logger.info(f"Receive request for {station_name}")
    try:
        if station_name == ARTEMIS_STATION['name']:
            return __artemis_interface_receive(AZURA_STATION)
        elif station_name == ELYSE_TERMINAL['name']:
            return await __elyse_interface_receive(AZURA_STATION)
        elif station_name == CORE_STATION['name']:
            return __core_interface_receive(AZURA_STATION)
        elif station_name == STATION_19_A['name']:
            return __station_19_a_interface_receive()
    except Exception as e:
        logger.error(f"Error in receive_data: {e}")
        return {"status": "Error", "message": f"{e}"}

    return {"status": "Error", "message": "Station not found"}


@app.route('/<station_name>/send', methods=['POST'])
async def send(station_name):
    logger.info(f"Send request for {station_name}")
    # Extract data from the request
    data = await request.get_json(force=True)

    if not data or 'source' not in data or 'data' not in data:
        return {"status": "Invalid request data"}

    try:
        if station_name == AZURA_STATION['name']:
            return __azura_interface_send(data['source'], data['data'])
    except Exception as e:
        logger.error(f"Error in send_data: {e}")
        return {"status": "Error sending data", "message": str(e)}

    return {"status": "Error", "message": "Station not found"}


def __station_19_a_interface_receive():
    response = json.loads(requests.get("http://192.168.100.19:2034/messages_for_other_stations").text)
    messages = []
    for dest, base64data in response['received_messages']:
        messages.append({"destination": dest, "data": list(base64.b64decode(base64data))})
    return {"kind": "success", "messages": messages}


def __artemis_interface_receive(destination_station):
    server_url = "http://192.168.100.19:2024/RPC2"
    proxy = xmlrpc.client.ServerProxy(server_url)

    response_receive = proxy.receive()

    messages = []
    for destination, data in response_receive:
        if destination == destination_station['name']:
            if isinstance(data, xmlrpc.client.Binary):
                data = data.data
            json_string = json.dumps(json.loads(data.decode('utf-8')))
            json_bytes = json_string.encode('utf-8')
            json_bytearray = bytearray(json_bytes)
            messages.append({"destination": destination_station['name'], "data": list(json_bytearray)})
    return {"kind": "success", "messages": messages}


async def __elyse_interface_receive(destination_station):
    server_url = "ws://192.168.100.19:2026/api"
    messages = []

    async with websockets.connect(server_url) as websocket:
        message = await websocket.recv()

        while True:
            response_data = json.loads(message)
            print(response_data)
            if response_data.get("destination") == destination_station['name']:
                messages.append({"destination": destination_station['name'], "data": list(response_data.get('msg'))})
                break

    return {"kind": "success", "messages": messages}

def __core_interface_receive(destination_station):
    received_messages = json.loads(requests.post(f"http://192.168.100.19:2027/receive").text).get(
        "received_messages")
    messages = []
    for message in received_messages:
        dest = message.get("target")

        if dest == destination_station['name']:
            msg = message.get("data")
            decoded_bytes = base64.b64decode(msg)
            messages.append({"destination": destination_station['name'], "data": list(decoded_bytes)})
    logger.info(f"core receive messages: {messages}")
    return {"kind": "success", "messages": messages}

def __azura_interface_send(source_station, msg):
    base64_encoded = base64.b64encode(bytearray(msg))
    base64_string = base64_encoded.decode('utf-8')
    data = {"sending_station": source_station, "base64data": base64_string}
    print(data)
    requests.post(f"http://192.168.100.19:2030/put_message", json=data)
    return {"kind": "success"}

def __core_interface_send(source_station, msg):
    base64_encoded = base64.b64encode(bytearray(msg))
    base64_string = base64_encoded.decode('utf-8')

    data = {"source": source_station, "message": base64_string}
    requests.post(f"http://192.168.100.19:2027/send", json=data)
    return {"kind": "success"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023, debug=True)
