import xmlrpc.client

# Der Endpoint der XML-RPC-Schnittstelle
url = 'http://192.168.100.19:2024/RPC2'

# Client erstellen, um mit der XML-RPC-Schnittstelle zu kommunizieren
client = xmlrpc.client.ServerProxy(url)

# Beispiel für die receive-Methode
try:
    # receive-Methode aufrufen
    messages = client.receive()
    print("Received messages:")
    for destination, message in messages:
        print(f"Destination: {destination}, Message: {message}")
except Exception as e:
    print(f"Error in receive: {e}")
