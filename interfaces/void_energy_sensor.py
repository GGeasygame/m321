import requests
import time
from pymongo import MongoClient

# MongoDB-Verbindung und Konfiguration
mongo_url = "mongodb://theship:theship1234@192.168.100.19:2021/theshipdb"
client = MongoClient(mongo_url)
db = client["theshipdb"]
collection = db["vacuum-energy"]

# Sensor-API-Konfiguration
trigger_url = "http://192.168.100.19:2037/trigger_measurement"


def trigger_measurement(request_id):
    """Löst eine Messung aus."""
    response = requests.post(trigger_url, json={"request_id": request_id})
    if response.status_code == 201:
        print("Messung ausgelöst.")
        return True
    else:
        print("Fehler beim Auslösen der Messung.")
        print(response.text)
        return False


def get_measurement_result(request_id, measurement_url):
    """Fragt das Messergebnis ab, bis es verfügbar ist, und gibt es zurück."""
    while True:
        response = requests.get(measurement_url)
        print(response.text)
        data = response.json()

        if data["state"] == "measured":
            print("Messergebnis erhalten:", data["result"])
            return data["result"]
        else:
            print("Messung läuft, warte auf Ergebnis...")
            time.sleep(1)  # Wartezeit zwischen den Abfragen


def save_to_mongodb(result):
    """Speichert das Messergebnis als Hex-String in MongoDB."""
    collection.update_one({}, {"$set": {"data": result}}, upsert=True)
    print("Ergebnis in MongoDB gespeichert.")


def delete_measurement(request_id, delete_url):
    """Löscht die Messung vom Server."""
    response = requests.delete(delete_url)
    if response.status_code == 200:
        print("Messung erfolgreich gelöscht.")
    else:
        print("Fehler beim Löschen der Messung.")


def shield():
    id_increment = 6
    while True:
        request_id = "my_id_" + str(id_increment)
        id_increment += 1
        if trigger_measurement(request_id):
            print(request_id)
            measurement_url = "http://192.168.100.19:2037/measurements/" + request_id
            delete_url = "http://192.168.100.19:2037/measurements/" + request_id
            print(f"measurement url {measurement_url} delete url {delete_url}")
            result = get_measurement_result(request_id, measurement_url)
            save_to_mongodb(result)
            delete_measurement(request_id, delete_url)
            print("Warte vor nächster Messung...")
            time.sleep(3)  # Zeitintervall zwischen den Messungen

