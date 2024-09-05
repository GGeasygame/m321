import requests

# Basis-URL des Servers
base_url = "http://192.168.100.19:2000"

# OAuth2-Konfiguration
def configure_oauth(client_secret, authorize_url, token_url):
    url = f"{base_url}/configure_oauth"
    data = {
        "client_secret": client_secret,
        "authorize_url": authorize_url,
        "token_url": token_url
    }
    response = requests.post(url, json=data)
    return response.json()

# Aktivieren des Systems
def activate_system():
    url = f"{base_url}/activate"
    response = requests.post(url)
    return response.json()

# Deaktivieren des Systems
def deactivate_system():
    url = f"{base_url}/deactivate"
    response = requests.post(url)
    return response.json()

# Einstellen des Winkels
def set_angle(angle):
    url = f"{base_url}/angle"
    data = {
        "angle": angle
    }
    response = requests.put(url, json=data)
    return response.json()

# Überprüfen des Status
def get_state():
    url = f"{base_url}/state"
    response = requests.get(url)
    return response.json()

# Beispielverwendung
if __name__ == "__main__":
    # Geben Sie hier Ihre Konfigurationsdetails ein
    client_secret = "mein_geheimer_schluessel"
    authorize_url = "http://http://192.168.100.19:2000:2015/authorize"
    token_url = "http://mein_auth_server:2015/token"

    # Konfiguration des OAuth2-Logins
    config_response = configure_oauth(client_secret, authorize_url, token_url)
    print("OAuth2-Konfiguration:", config_response)

    # System aktivieren
    activate_response = activate_system()
    print("System aktiviert:", activate_response)

    # Winkel einstellen
    angle_response = set_angle(42)
    print("Winkel eingestellt:", angle_response)

    # Status überprüfen
    state_response = get_state()
    print("Systemstatus:", state_response)

    # System deaktivieren (optional)
    deactivate_response = deactivate_system()
    print("System deaktiviert:", deactivate_response)
