import requests
import json

# Die URL des Endpunkts
url = "http://192.168.100.19:2030/put_message"

# Die Daten, die an den Server gesendet werden
payload = {
    "sending_station": "Shangris Station",
    "base64data": "Rm9yc2NodW5nc2RhdGVuIChHcnVwcGUgMTkyLjE2OC4xMDAuMTkp="
}

# Header (falls benötigt)
headers = {
    "Content-Type": "application/json"
}

try:
    # POST-Anfrage senden
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
except Exception as e:
    print(f"An error occurred: {e}")
