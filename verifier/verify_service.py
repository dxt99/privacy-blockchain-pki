import config
from model import Transaction
from chain_service import ChainService
from typing import List, Tuple
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class VerifyService:
    def __init__(self):
        self.chain = ChainService()
        
    def verify(self, transactions: dict) -> bool:
        if not len(transactions) : return False
        
        sorted_tx: List[Tuple[int, Transaction]] = [(id, transaction) for id, transaction in transactions.items()]
        sorted_tx.sort()
        id: int = sorted_tx[0][0]
        register_tx: Transaction = sorted_tx[0][1]
        cname = register_tx.identity
        
        # Verify registration
        res = self.__verify_single(id, register_tx, cname)
        previous_key = register_tx.public_key
        
        for id, transaction in sorted_tx[1:]:
            res &= self.__verify_single(id, transaction, previous_key)
            previous_key = transaction.public_key
        return res
    
    def __verify_single(self, id: int, transaction: Transaction, data: str) -> bool:
        if self.chain.is_revoked(id):
            return False
        chain_tx = self.chain.get_transaction(id)
        if chain_tx != transaction:
            print("Transaction not matching chain records")
            return False
    
        # parsing pub key
        try: 
            pub_key = serialization.load_pem_public_key(bytes.fromhex(transaction.public_key))
            data_signature = transaction.signature_parse()[0]
        except:
            print("Failed to parse public key")
            return False
        
        # verifying registration
        if len(transaction.identity) != 0:
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

        # verifying updates
        if len(transaction.signature_parse()) != 2:
            print("Signature count is wrong, expected two signatures")
            return False
        # verifying first signature
        try:
            pub_key.verify(data_signature, bytes.fromhex(transaction.public_key),
                        algorithm=hashes.SHA256(),
                        padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH))
        except:
            print("Failed to verify first online signature")
            return False
    
        # verifying second signature
        try:
            data_signature = transaction.signature_parse()[1]
            decrypted_signature = config.verifier_key.decrypt(
                data_signature,
                padding=padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                ))
        except:
            print("Failed to decrypt second signature")
            return False
        try:
            pub_key.verify(decrypted_signature, bytes.fromhex(data),
                        algorithm=hashes.SHA256(),
                        padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH))
            return True
        except:
            print("Failed to verify second online signature")
            return False
        