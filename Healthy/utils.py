import configparser
from datetime import datetime
import requests


def error_msg(api, err):
    """
    This function returns the error message
    :param api: what api did you try to reach
    :param err: error code you got
    :return: error message
    """
    return f"Error: Could not get {api}, request failed with status code - {err}"


def get_token():
    """
    This function returns the token from the config file
    :return: NPM token
    """
    config = configparser.ConfigParser()
    config.read('../config.ini')
    return config['NPM']['token']


def get_version_date(date):
    """
    This function returns the health status of the package in terms of version date
    :param date: latest version date (string)
    :return: if no issues found will return healthy else will return the issue message
    """
    if (datetime.now() - date).days > 30:
        return "Last version is more than 30 days old"
    else:
        return "healthy"


def get_number_maintainers(number):
    """
    This function returns the health status of the package in terms of number of maintainers
    :param number: number of maintainers as returned by the api (int)
    :return: if no issues found will return healthy else will return the issue message
    """
    if number < 2:
        return "Number of maintainers is less than 2"
    else:
        return "healthy"


def get_latest_commit(commit_date):
    """
    This function returns the health status of the package in terms of latest commit date
    :param commit_date: latest commit date (string)
    :return: if no issues found will return healthy else will return the issue message
    """
    if (datetime.now() - commit_date).days > 14:
        return "Latest commit is more than 14 days old"
    else:
        return "healthy"


def analyze_health(last_version_date, maintainers, last_commit_date):
    """
    This function analyzes the messages got by other functions and returns the final message to be displayed
    :param last_version_date: message from get_version_date function
    :param maintainers: message from get_number_maintainers function
    :param last_commit_date: message from get_latest_commit function
    :return: final message to be displayed (if healthy will return empty list)
    """
    message = []
    if last_version_date != "healthy":
        message.append("Last version is more than 30 days old ")
    if maintainers != "healthy":
        message.append("Number of maintainers is less than 2 ")
    if last_commit_date != "healthy":
        message.append("Latest commit is more than 14 days old")
    return message


def build_base_url_npm(name):
    """
    This function builds the base url for the api call
    :param name: package name to build url for
    :return: target url
    """
    return f"https://registry.npmjs.org/{name}"


def get_package_info(base_url, token, name):
    """
    This function returns the package info from the api call
    :param base_url: url to request on
    :param token: npm access token
    :param name: package name
    :return: dictionary with package info and status code
    """
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
    """
    This function returns the repo info for npm packages
    :param name: package name
    :return: dictionary with package info and status code
    """
    base_url = build_base_url_npm(name)
    token = get_token()
    repo_info = get_package_info(base_url, token, name)

    return repo_info