import requests
from flask import Flask
app = Flask(__name__)

@app.route(rule="/", methods=["GET"])
def get_data():
    try:
        response = requests.get("http://192.168.100.19:2038/data")
        json = response.json()
        return {"data": json.get("result")}
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2101)