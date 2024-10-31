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
import asyncio
import threading

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Quart(__name__)

PERMASTORE_URL = 'http://192.168.100.19:2019'

ZURRO_STATION = {"x": 5608, "y": 9386, "name": "Zurro Station"}
VESTA_STATION = {"x": 10000, "y": 10000, "name": "Vesta Station"}
CORE_STATION = {"x": 0, "y": 0, "name": "Core Station"}
AZURA_STATION = {"x": -1000, "y": 1000, "name": "Azura Station"}
STATION_18_A = {"x": 15534, "y": 14401, "name": "Station 18-A"}
STATION_19_A = {"x": -15526, "y": -12527, "name": "Station 19-A"}
STATION_20_A = {"x": 12903, "y": -17816, "name": "Station 20-A"}
SHANGRIS_STATION = {"x": 4143, "y": 4808, "name": "Shangris Station"}
GOLD_STONE = {"x": -9800, "y": 20200, "name": "Gold Stone"}
ARTEMIS_STATION = {"x": -20000, "y": 38000, "name": "Artemis Station"}
ELYSE_TERMINAL = {"x": 72701, "y": -78179, "name": "Elyse Terminal"}


async def receive_stations():
    while True:
        logger.info("new receives for stations 18-a, 19-a, 20-a")
        try:
            __station_19_a_interface_receive()
        except Exception as e:
            logger.error(f"Error when receiving 19-A {e}")
        await asyncio.sleep(5)


def __station_20_a_interface_receive():
    response = requests.post(f"192.168.100.20:2023/{STATION_20_A['name']}/receive")
    logger.info(f"receive Station 20: {response}")
    return response


def __station_18_a_interface_receive():
    response = requests.post(f"http://192.168.100.18:2023/{STATION_18_A['name']}/receive")
    logger.info(f"receive Station 18: {response}")
    return response


def __station_20_a_interface_send(source_station, message):
    data = {"source": source_station, "data": message}
    logger.info(f"send Station 20: {message}")
    response = requests.post(f"http://192.168.100.20:2023/{STATION_20_A['name']}/send", json=data)
    return response


def __station_18_a_interface_send(source_station, message):
    data = {"source": source_station, "data": message}
    logger.info(f"send Station 18: {message}")
    response = requests.post(f"http://192.168.100.18:2023/{STATION_18_A['name']}/send", json=data)
    return response


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
        elif station_name == AZURA_STATION['name']:
            return __azura_interface_receive()
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
        logger.error("invalid request data")
        return {"status": "Invalid request data"}

    try:
        if station_name == AZURA_STATION['name']:
            return __azura_interface_send(data['source'], data['data'])
        elif station_name == CORE_STATION['name']:
            return __core_interface_send(data['source'], data['data'])
        elif station_name == STATION_18_A['name']:
            return __station_18_a_interface_send(data['source'], data['data'])
        elif station_name == STATION_19_A['name']:
            return __station_19_a_interface_send(data['source'], data['data'])
        elif station_name == STATION_20_A['name']:
            return __station_20_a_interface_send(data['source'], data['data'])
    except Exception as e:
        logger.error(f"Error in send_data: {e}")
        return {"status": "Error sending data", "message": str(e)}

    return {"status": "Error", "message": "Station not found"}


def __station_19_a_interface_receive():
    response = json.loads(requests.get("http://192.168.100.19:2034/messages_for_other_stations").text)
    messages = []
    for msg in response['received_messages']:
        dest = msg['dest']
        base64data = msg['base64data']
        logger.debug(f"destination {dest} data {base64data}")
        messages.append({"destination": dest, "data": list(base64.b64decode(base64data))})
    for message in messages:
        logger.info(f"receive Station 19: {message}")
        data = {"source": STATION_19_A['name'], "data": message['data']}
        if message['destination'] == STATION_18_A['name']:
            __station_18_a_interface_send(data['source'], data['data'])
        elif message['destination'] == STATION_20_A['name']:
            __station_20_a_interface_send(data['source'], data['data'])
    return {"kind": "failed"}


def __azura_interface_receive():
    response = json.loads(requests.get("http://192.168.100.19:2030/messages_for_other_stations").text)
    messages = []
    for response in response['received_messages']:
        base64data = response['base64data']
        dest = response['dest']
        # encoded = list(base64.b64decode(base64data))
        messages.append({"destination": dest, "data": base64data})
    for message in messages:
        logger.info(f"receive Azura Station: {message}")
        # data = {"source": AZURA_STATION['name'], "data": message['data']}
        __core_interface_send(AZURA_STATION['name'], message)
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
        dest = message["target"]

        if dest == destination_station['name']:
            msg = message["data"]
            logger.debug(f"core receive message {msg}")
            # decoded_bytes = list(base64.b64decode(msg))
            messages.append({"destination": destination_station['name'], "data": msg})
            __azura_interface_send(CORE_STATION['name'], msg)
    logger.info(f"core receive messages: {messages}")
    return {"kind": "success", "messages": messages}


def __station_19_a_interface_send(source_station, msg):
    logger.info(f"Station 19-A message before transformation {msg}")
    base64_encoded = base64.b64encode(bytearray(msg))
    base64_string = base64_encoded.decode('utf-8')
    data = {"sending_station": source_station, "base64data": base64_string}
    logger.info(f"{source_station} send to station-19-a messages: {base64_string} ({msg})")
    requests.post("http://192.168.100.19:2034/put_message", json=data)
    return {"kind": "success"}


def __azura_interface_send(source_station, msg):
    # base64_encoded = base64.b64encode(bytearray(msg))
    # base64_string = base64_encoded.decode('utf-8')
    data = {"sending_station": source_station, "base64data": msg}
    requests.post(f"http://192.168.100.19:2030/put_message", json=data)
    # logger.info(f"azura send messages: {base64_string} ({msg})")
    logger.info(f"azura send messages: {msg}")
    return {"kind": "success"}

def __core_interface_send(source_station, msg):
    # base64_encoded = base64.b64encode(bytearray(msg))
    # base64_string = base64_encoded.decode('utf-8')

    data = {"source": source_station, "message": msg}
    requests.post(f"http://192.168.100.19:2027/send", json=data)
    # logger.info(f"core send messages: {base64_string} ({msg})")
    logger.info(f"core send messages: {msg}")
    return {"kind": "success"}


def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

@app.before_serving
async def startup():
    app.add_background_task(receive_stations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023, debug=True)
