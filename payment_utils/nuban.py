import time
import requests
from decouple import config
from django.http import JsonResponse
import uuid
import payment_utils.env as env

CACHED_KUDA_TOKEN = None
CACHED_KUDA_TOKEN_EXPIRY = time.time() + 100


class Nuban:
    def __init__(self):
        self.api_key = env.KUDA_API_KEY
        self.api_email = env.KUDA_API_EMAIL
        self.access_token = env.KUDA_ACCESS_KEY
        self.test_url = "http://kuda-openapi-uat.kudabank.com/v2.1"
        self.prod_url = "https://kuda-openapi.kuda.com/v2.1"
        self.admin_account_number = "3000917707"
        self.serviceEndpoint = ""
        self.serviceType = ""

    def get_token(self):
        global CACHED_KUDA_TOKEN, CACHED_KUDA_TOKEN_EXPIRY
        if CACHED_KUDA_TOKEN is not None and CACHED_KUDA_TOKEN_EXPIRY > time.time():
            return CACHED_KUDA_TOKEN
        endpoint = "/Account/GetToken"
        data = {"email": self.api_email, "apiKey": self.api_key}
        response = requests.post(self.test_url + endpoint, json=data)
        if response.status_code == 200:
            CACHED_KUDA_TOKEN = response.text
            CACHED_KUDA_TOKEN_EXPIRY = time.time() + 82800  # Expire in 23 hours
            return response.text
        raise ValueError(f'{response.headers.get("WWW-Authenticate")}')

    def send_request(self, data: dict | None = None):
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/JSON",
        }
        payload = {"serviceType": self.serviceType, "requestref": str(uuid.uuid4())}
        if data:
            payload["Data"] = data

        response = requests.post(
            url=self.test_url + self.serviceEndpoint, headers=headers, json=payload
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f'{response.headers.get("WWW-Authenticate")}')

    def get_admin_balance(self):
        self.serviceType = "ADMIN_RETRIEVE_MAIN_ACCOUNT_BALANCE"
        res = self.send_request()
        return res["availableBalance"]

    def fetch_banks(self):
        self.serviceType = "BANK_LIST"
        res = self.send_request()
        return res["data"]["banks"]

    def get_bank_name(self, bank_code):
        banks = self.fetch_banks()
        for bank in banks:
            if bank['bankCode'] == bank_code:
                return bank['bankname']
        return 'Dummy'

    def name_enquiry(self, number, bank_code) -> tuple:
        """
        returns search bool, account_name (account_name is '' if search is False)
        """
        self.serviceType = "NAME_ENQUIRY"
        data = {"BeneficiaryAccountNumber": number, "BeneficiaryBankCode": bank_code}
        res = self.send_request(data)
        try:
            return res["status"], res["data"]["beneficiaryName"]
        except Exception as e:
            return False, e

    def generate_virtual_account(self, name):
        self.serviceType = "ADMIN_CREATE_DYNAMIC_COLLECTION_ACCOUNT"
        data = {"Amount": 10000000, "AccountName": name, "IsPassThrough": True}
        res = self.send_request(data)
        return res

    def initiate_transfer(self, amount, number, bank_code) -> tuple:
        name_query, name = self.name_enquiry(number, bank_code)
        if name_query:
            self.serviceType = "SINGLE_FUND_TRANSFER"
            data = {
                "BeneficiaryAccount": number,
                "beneficiaryBankCode": bank_code,
                "amount": amount,
                "ClientAccountNumber": self.admin_account_number,
                "beneficiaryName": name,
                "narration": "Service Payment",
                "SenderName": "Wedigital Devs",
            }
            res = self.send_request(data)
            return {
                "status": res["status"],
                "message": res["message"],
                "ref": res["transactionReference"],
            }
        return False, "Name enquiry failed"
