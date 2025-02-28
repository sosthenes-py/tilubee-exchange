import time
import requests
from decouple import config
from django.http import JsonResponse
import uuid

CACHED_KUDA_TOKEN = None


class Nuban:
    def __init__(self):
        self.api_key = config("KUDA_API_KEY")
        self.api_email = config("KUDA_API_EMAIL")
        self.access_token = config("KUDA_ACCESS_TOKEN")
        self.base_url = "http://kuda-openapi-uat.kudabank.com/v2.1"
        self.serviceEndpoint = ""

    def get_token(self):
        endpoint = "/Account/GetToken"
        data = {"email": self.api_email, "apiKey": self.api_key}
        response = requests.post(self.base_url + endpoint, json=data)
        if response.status_code == 200:
            return response.text
        return response

    def send_request(self, data):
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/JSON",
        }
        response = requests.post(
            url=self.base_url + self.serviceEndpoint, headers=headers, json=data
        )
        return response.json()

    def get_admin_balance(self):
        data = {
            "serviceType": "ADMIN_RETRIEVE_MAIN_ACCOUNT_BALANCE",
            "requestref": str(uuid.uuid4()),
        }
        return self.send_request(data)
