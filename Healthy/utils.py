import configparser
from datetime import datetime
import requests


def error_msg(api, err):
    return f"Error: Could not get {api}, request failed with status code - {err}"


def get_token():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    return config['NPM']['token']


def get_version_date(date):
    if (datetime.now() - date).days > 30:
        return "Last version is more than 30 days old"
    else:
        return "healthy"


def get_number_maintainers(number):
    if number < 2:
        return "Number of maintainers is less than 2"
    else:
        return "healthy"


def get_latest_commit(commit_date):
    if (datetime.now() - commit_date).days > 14:
        return "Latest commit is more than 14 days old"
    else:
        return "healthy"


def analyze_health(last_version_date, maintainers, last_commit_date):
    message = []
    if last_version_date != "healthy":
        message.append("Last version is more than 30 days old ")
    if maintainers != "healthy":
        message.append("Number of maintainers is less than 2 ")
    if last_commit_date != "healthy":
        message.append("Latest commit is more than 14 days old")
    return message


def build_base_url_npm(name):
    return f"https://registry.npmjs.org/{name}"


def get_package_info(base_url, token, name):
    time_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    header = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(base_url, headers=header)
    if response.status_code == 200:
        latestVersion = response.json()['dist-tags']['latest']
        latestVersionDate = datetime.strptime(response.json()['time'][latestVersion], time_format)

        numberOfMaintainers = len(response.json()['maintainers'])

        latestCommittedDate = datetime.strptime(response.json()['time']['modified'], time_format)

        repo_info = {
            "name": name,
            "version_date": get_version_date(latestVersionDate),
            "num_maintainers": get_number_maintainers(numberOfMaintainers),
            "latest_commit": get_latest_commit(latestCommittedDate),
            "status_code": 200
        }
    else:
        repo_info = {
            "name": name,
            "version_date": error_msg("version date", response.status_code),
            "num_maintainers": error_msg("number of maintainers", response.status_code),
            "latest_commit": error_msg("latest commit", response.status_code),
            "status_code": response.status_code
        }

    return repo_info


def get_repo_info_npm(name):
    base_url = build_base_url_npm(name)
    token = get_token()
    repo_info = get_package_info(base_url, token, name)

    return repo_info