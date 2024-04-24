import json
from dataclasses import dataclass

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
    
if __name__ == '__main__':
    tr = Transaction("a", "b", "c")
    print(tr.to_json_string())