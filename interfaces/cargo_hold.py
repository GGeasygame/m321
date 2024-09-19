import json
import requests
import time


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
            print(f"Credits: {data['hold']['credits']}")
            print(f"Gesamtkapazität: {data['hold']['hold_size']}")
            print(f"Freie Kapazität: {data['hold']['hold_free']}")
            print("Ressourcen im Lager:")
            for resource, amount in data["hold"]["resources"].items():
                print(f"{resource}: {amount}")

    def swap_adjacent(self, x1, y1, x2, y2):
        retries = 0
        while True:
            if retries > 10:
                break
            url = f"{self.base_url}/swap_adjacent"
            response = requests.post(url, data=json.dumps({
                "a": {"x": x1, "y": y1},
                "b": {"x": x2, "y": y2}
            }))
            print(str(response.json()) + f" x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")
            if response.status_code == 200:
                return response.json()
            time.sleep(0.4)
            retries += 1

    def get_structure(self):
        url = f"{self.base_url}/structure"
        return requests.get(url).json()

    def swap_rows(self, y1, y2):
        structure = self.get_structure()
        horizontal_length = len(structure['hold'][0])

        for i in range(horizontal_length):
            self.swap_adjacent(i, y1, i, y2)

    async def swap_to_lowest_available(self):
        structure = self.get_structure()
        vertical_height = 0

        for i in range(len(structure['hold'])):
            if structure['hold'][i][0] is None:
                vertical_height = i

        if vertical_height == 0:
            return False

        for i in range(vertical_height):
            self.swap_rows(i, i + 1)
        return True
