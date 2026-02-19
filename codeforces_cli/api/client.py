import requests

BASE_URL = "https://codeforces.com/api/"


def fetch(endpoint: str, params: dict = None):
    url = BASE_URL + endpoint
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Failed to connect to Codeforces API")
    data = response.json()
    if data["status"] != "OK":
        raise Exception("Codeforces API returned error")

    return data["result"]
