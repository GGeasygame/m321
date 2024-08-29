import requests


def download_data(source, destination):
    response = requests.post("http://192.168.100.19:2019/download",
                             data='{"source": "' + source + '", "destination": "' + destination + '"}')

    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve data"}


download_data("Zurro Station", "Azura Station")
