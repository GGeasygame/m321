class CargoHold:
    def __init__(self, capacity):
        self.capacity = capacity  # Maximale Kapazität des Frachtraums
        self.used_capacity = 0  # Aktuell genutzte Kapazität
        self.credits = 20  # Startguthaben
        self.items = []  # Liste der Gegenstände im Frachtraum

    def add_item(self, item_name, description, size):
        if self.used_capacity + size > self.capacity:
            return "Nicht genug Platz im Frachtraum!"
        else:
            self.items.append({"name": item_name, "description": description, "size": size})
            self.used_capacity += size
            return f"{item_name} wurde hinzugefügt."

    def remove_item(self, item_name):
        for item in self.items:
            if item["name"] == item_name:
                self.items.remove(item)
                self.used_capacity -= item["size"]
                return f"{item_name} wurde entfernt."
        return f"{item_name} nicht gefunden."

    def list_items(self):
        if not self.items:
            return "Der Frachtraum ist leer."
        return "\n".join([f"{item['name']} - {item['description']} (Größe: {item['size']})" for item in self.items])

    def buy_item(self, item_name, description, price, size):
        if self.credits < price:
            return "Nicht genug Credits!"
        if self.used_capacity + size > self.capacity:
            return "Nicht genug Platz im Frachtraum!"
        self.credits -= price
        self.add_item(item_name, description, size)
        return f"{item_name} wurde gekauft und hinzugefügt."

    def sell_item(self, item_name, price):
        for item in self.items:
            if item["name"] == item_name:
                self.items.remove(item)
                self.used_capacity -= item["size"]
                self.credits += price
                return f"{item_name} wurde verkauft."
        return f"{item_name} nicht gefunden."

    def show_status(self):
        return f"Credits: {self.credits}, Genutzte Kapazität: {self.used_capacity}/{self.capacity}"

# Beispielhafte Nutzung
cargo = CargoHold(capacity=12)

# Gegenstände hinzufügen
print(cargo.add_item("Permastore", "Modul, um Daten zu transferieren", 1))
print(cargo.add_item("Scanner TX1000", "Scannt was das Zeug hält", 2))

# Gegenstände auflisten
print(cargo.list_items())

# Gegenstand kaufen
print(cargo.buy_item("Abbaulaser", "Laser, um Hindernisse aus dem Weg zu räumen", 5, 3))

# Status anzeigen
print(cargo.show_status())

# Gegenstand verkaufen
print(cargo.sell_item("Scanner TX1000", 2))

# Status nach Verkauf anzeigen
print(cargo.show_status())
