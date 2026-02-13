import requests

class CubeClient:
    def __init__(self, url):
        self.url = url

    def get_meta(self):
        r = requests.get(f"{self.url}/meta")
        return r.json()

    def run_query(self, body):
        r = requests.post(f"{self.url}/load", json=body)
        return r.json()
