from opcua import Client, ua

url = "opc.tcp://192.168.100.19:2035/"
client = Client(url)

def connect_to_opcua():
    try:
        client.connect()
        print("Verbunden mit OPC UA Server")

        node = client.get_node("ns=0;i=20001")
        print(f"Node Name: {node.get_browse_name()}")
    except Exception as e:
        print(f"Fehler bei der Verbindung zum OPC UA Server: {e}")

def jump_to(x, y):
    try:
        node = client.get_node("ns=0;i=20001")

        # Verwende die to_variant Funktion für die Argumente
        result = node.call_method("0:JumpTo", ua.Variant(x, ua.VariantType.Int32), ua.Variant(y, ua.VariantType.Int32))

        print(f"Ergebnis von JumpTo: {result}")

    except Exception as e:
        print(f"Fehler bei JumpTo: {e}")

def get_charge_percent():
    try:
        # Hole die Methode GetChargePercent
        node = client.get_node("ns=0;i=20001")

        # Rufe die Methode auf
        result = node.call_method("0:GetChargePercent")

        print(f"Ladestand in Prozent: {result}")

    except Exception as e:
        print(f"Fehler bei GetChargePercent: {e}")