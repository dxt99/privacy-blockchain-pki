import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class Transaction:
    identity: str
    public_key: str
    signatures: str
    
    def to_dict(self) -> dict:
        payload = {
            'identity': self.identity,
            'public_key': self.public_key,
            'signatures': self.signatures
        }
        return payload
    
    @staticmethod
    def from_json_string(transaction_json: dict):
        identity = transaction_json["identity"]
        public_key = transaction_json["public_key"]
        signatures = transaction_json["signatures"]
        return Transaction(identity, public_key, signatures)
    
    @staticmethod
    def parse_transaction_list(transaction_json_list: dict):
        result = {}
        for key, value in transaction_json_list.items():
            id = int(key)
            transaction = Transaction.from_json_string(value)
            result[id] = transaction
        return result
