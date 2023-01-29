import configparser
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('../config.ini')
my_port = config['Resty']['port']
my_host = config['Resty']['host']
healthy_port = config["Healthy"]["port"]
healthy_host = config["Healthy"]["host"]


@app.route("/packages", methods=["POST"])
def check_packages():
    # if request.is_json:
    package = request.get_json()
    # pass the packages to the "Healthy" microservice for processing
    response = requests.post(f"http://{healthy_host}:{healthy_port}/process", json={"packages": package['data']})
    if response.status_code != 200:
        return jsonify({"error": "Failed to communicate with the Healthy microservice"}), 500
    result = response.json()
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True, port=my_port, host=my_host)
