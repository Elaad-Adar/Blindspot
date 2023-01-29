from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
import configparser

from Healthy.utils import get_repo_info_npm, analyze_health

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('../config.ini')
my_host = config['Healthy']['host']
my_port = config['Healthy']['port']


def check_security_health(packages):
    results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        # submit the package checking task to the executor
        for package in packages:
            results.append(executor.submit(get_repo_info_npm, package))
    # wait for all tasks to complete
    result = {}
    for f in results:
        try:
            repo_data = f.result()
            if repo_data['status_code'] != 200:
                result[repo_data["name"]] = "Package not found"
                continue
            else:
                result[repo_data["name"]] = "Package is healthy"
                # process the result and check for security health
                last_version_date = repo_data["version_date"]
                maintainers = repo_data['num_maintainers']
                last_commit_date = repo_data['latest_commit']
                message = analyze_health(last_version_date, maintainers, last_commit_date)
                if message:
                    result[repo_data["name"]] = "package unhealthy due to -" + 'and '.join(message)
        except Exception as e:
            result[repo_data["name"]] = f"Error occurred: {e}"

    return result


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    # process the parameters and check for security health
    packages = data["packages"]
    if len(packages) > 10:
        return jsonify({"error": "You can only process 10 packages at a time"}), 400
    result = check_security_health(packages)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host=my_host, port=my_port)
