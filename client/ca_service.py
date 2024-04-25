import config
import requests
from model import Transaction
from typing import Tuple

class CaService:
    @staticmethod
    def register_transaction(transaction: Transaction) -> bool:
        url = f"{config.ca_base_url}/register"
        transaction_dict = transaction.to_dict()
        res = requests.post(url, json = transaction_dict)
        try:
            payload = res.status_code
            return payload == 200
        except:
            print(res.content, res.text)
            return False

    @staticmethod    
    def transaction_status(transaction: Transaction) -> Tuple[str, int]:
        url = f"{config.ca_base_url}/status"
        transaction_dict = transaction.to_dict()
        res = requests.post(url, json = transaction_dict)
        try:
            payload = res.json()
            return str(payload["status"]), int(payload["id"])
        except:
            return "Failed to get status from CA"
