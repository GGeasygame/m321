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
measurement_url = "http://192.168.100.19:2037/measurements/my_id_001"
delete_url = "http://192.168.100.19:2037/measurements/my_id_001"


def trigger_measurement(request_id):
    """Löst eine Messung aus."""
    response = requests.post(trigger_url, json={"request_id": request_id})
    if response.status_code == 201:
        print("Messung ausgelöst.")
        return True
    else:
        print("Fehler beim Auslösen der Messung.")
        return False


def get_measurement_result(request_id):
    """Fragt das Messergebnis ab, bis es verfügbar ist, und gibt es zurück."""
    while True:
        response = requests.get(measurement_url)
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


def delete_measurement(request_id):
    """Löscht die Messung vom Server."""
    response = requests.delete(delete_url)
    if response.status_code == 200:
        print("Messung erfolgreich gelöscht.")
    else:
        print("Fehler beim Löschen der Messung.")


def shield():
    request_id = "my_id_001"
    while True:
        if trigger_measurement(request_id):
            result = get_measurement_result(request_id)
            save_to_mongodb(result)
            delete_measurement(request_id)
            print("Warte vor nächster Messung...")
            time.sleep(5)  # Zeitintervall zwischen den Messungen
