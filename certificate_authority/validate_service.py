import config
from model import Transaction
from chain_service import ChainService
from typing import List, Tuple
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

class ValidateService:
    def __init__(self):
        self.chain = ChainService()
    
    def validate(self, transaction: Transaction) -> bool:
        # parsing pub key
        try: 
            pub_key = serialization.load_pem_public_key(bytes.fromhex(transaction.public_key))
            data_signature = transaction.signature_parse()[0]
        except:
            print("Failed to parse public key")
            return False
        
        # verifying registration
        if len(transaction.identity) == 0:
            print("Identity not found")
            return False
        
        if len(transaction.signature_parse()) != 1:
            print("Signature count is wrong, expected one signature")
            return False
        
        try:
            pub_key.verify(data_signature, bytes.fromhex(transaction.public_key), 
                            algorithm=hashes.SHA256(),
                            padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH))
            return True
        except:
            print("Failed to verify online signature")
            return False
        