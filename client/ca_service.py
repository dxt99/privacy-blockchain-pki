import config
import requests
from model import Transaction
from typing import Tuple

class CaService:
    @staticmethod
    def register_transaction(transaction: Transaction):
        url = f"{config.ca_base_url}/register"
        transaction_dict = transaction.to_dict()
        res = requests.post(url, json = transaction_dict)
        try:
            payload = res.status_code
            assert(payload == 200)
        except:
            raise Exception(f"Failed to register transaction to CA: {res.text}")

    @staticmethod    
    def transaction_status(transaction: Transaction) -> Tuple[str, int]:
        url = f"{config.ca_base_url}/status"
        transaction_dict = transaction.to_dict()
        res = requests.post(url, json = transaction_dict)
        try:
            payload = res.json()
            return str(payload["status"]), int(payload["id"])
        except Exception as e:
            raise Exception(f"Failed to get transaction status from CA: {res.text}")
        
    @staticmethod
    def revocation_request(transaction: Transaction) -> str:
        url = f"{config.ca_base_url}/revoke/request"
        transaction_dict = transaction.to_dict()
        res = requests.post(url, json = transaction_dict)
        if res.status_code != 200:
            print(res.text)
            raise Exception("Failed to request revoke transaction")
        return res.text
    
    @staticmethod
    def revocation_challenge(transaction: Transaction, signature: str) -> str:
        url = f"{config.ca_base_url}/revoke/challenge"
        transaction_dict = transaction.to_dict()
        payload = {
            'challenge_signature': signature,
            'transaction': transaction_dict
        }
        res = requests.post(url, json = payload)
        if res.status_code != 200:
            print(res.text)
            raise Exception("Failed to request revoke transaction")
        return res.text