import requests

class CargoHoldAPI:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_cargo_hold_status(self):
        url = f"{self.base_url}/hold"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to retrieve data"}
    
    def display_status(self):
        data = self.get_cargo_hold_status()
        if "error" in data:
            print(data["error"])
        else:
            print("Status des Cargo Holds:")
            print(f"Credits: {data['credits']}")
            print(f"Gesamtkapazität: {data['hold_size']}")
            print(f"Freie Kapazität: {data['hold_free']}")
            print("Ressourcen im Lager:")
            for resource, amount in data["hold"]["resources"].items():
                print(f"{resource}: {amount}")

