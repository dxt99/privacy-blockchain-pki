import config
from key_manager import KeyManager
from ca_service import CaService
from chain_service import ChainService
from verify_service import VerifyService
from model import Transaction
from typing import Dict
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

class TransactionService:
    chain_service: ChainService
    key_manager: KeyManager
    
    name: str
    register_transaction: Transaction
    register_transaction_id: int
    update_transactions: Dict[int, Transaction]
    verifier_key: rsa.RSAPublicKey

    def __init__(self):
        self.name = config.client_common_name
        self.key_manager = KeyManager()
        self.chain_service = ChainService()
        self.verifying_service = VerifyService()
        self.register_transaction = None
        self.register_transaction_id = -1
        self.update_transactions = {}
        self.verifier_key = None
    
    @staticmethod
    def __serialize_signatures(*signatures: bytes):
        return f'({",".join([i.hex() for i in signatures])})'
    
    def __get_verifier_key(self):
        if self.verifier_key != None: return
        try: 
            transaction = self.chain_service.get_transaction(config.verifier_tx_id)
            self.verifier_key = serialization.load_pem_public_key(bytes.fromhex(transaction.public_key))
        except Exception as e:
            print("Failed to parse verifier public key")
            raise e
    
    def generate_and_register(self):
        if self.register_transaction != None:
            status, _ = self.register_request_status()
            if status != "Revoked":
                raise Exception("Cannot generate new key when old one is not revoked yet")
        self.register_transaction = None
        self.key_manager.new_key_chain()
        
        online_key = self.key_manager.base_key
        public_key = KeyManager.public_key_str(online_key)
        online_signature: bytes = KeyManager.sign(online_key, bytes.fromhex(public_key))
        signatures: str = self.__serialize_signatures(online_signature)
        
        register_transaction = Transaction(
            identity = self.name,
            public_key = public_key,
            signatures = signatures
        )
        
        CaService.register_transaction(register_transaction)
        self.register_transaction = register_transaction
    
    def update_key(self, pub_key_str: str = "") -> Dict[int, Transaction]:
        self.__get_verifier_key()
        if self.register_request_status() != "Approved":
            raise Exception("Cannot update key, registration not approved yet")
        if not self.register_transaction:
            raise Exception("Cannnot udpate key, no registration found")
        
        new_key = self.key_manager.add_key_to_chain()
        public_key = KeyManager.public_key_str(new_key)
        prev_data = bytes.fromhex(self.register_transaction.public_key)
        
        previous_signature: bytes = KeyManager.sign(new_key, prev_data)
        encryption_key = self.verifier_key
        if len(pub_key_str) > 0:
            try:
                encryption_key = serialization.load_pem_public_key(bytes.fromhex(pub_key_str))
            except:
                raise Exception(f"Failed to deserialize encryption key {pub_key_str}")
        try:
            encrypted_signature: bytes = KeyManager.encrypt(encryption_key, previous_signature)
        except:
            raise Exception("Failed to encrypt signature, key size is too small")
        online_signature: bytes = KeyManager.sign(new_key, bytes.fromhex(public_key))
        
        signatures: str = self.__serialize_signatures(online_signature, encrypted_signature)
        update_transaction = Transaction(
            identity = "",
            public_key = public_key,
            signatures = signatures
        )
        id = self.chain_service.update(update_transaction)
        self.update_transactions[id] = update_transaction
        return {
            self.register_transaction_id: self.register_transaction,
            id: update_transaction
        }
    
    def register_request_status(self) -> str:
        if self.register_transaction == None:
            return "No transaction found"
        res, id = CaService.transaction_status(self.register_transaction)
        if res == 'Approved':
            self.register_transaction_id = id
        else:
            self.register_transaction_id = -1
        return res
    
    def get_transactions(self) -> Dict[int, Transaction]:
        self.register_request_status()
        if self.register_transaction_id == -1:
            return self.update_transactions
        res = {self.register_transaction_id: self.register_transaction}
        res.update(self.update_transactions)
        return res
    
    def revoke_key(self) -> bool:
        status, _ = self.register_request_status()
        if status != "Approved":
            raise Exception("No approved key found")
        challenge = CaService.revocation_request(self.register_transaction)
        key = self.key_manager.base_key
        signature = self.key_manager.sign(key, bytes.fromhex(challenge))
        CaService.revocation_challenge(self.register_transaction, signature.hex())
        return True
    
    def verify(self, transactions: dict) -> bool:
        return self.verifying_service.verify(transactions, self.key_manager.base_key)

if __name__ == '__main__':
    print(TransactionService.__serialize_signatures(b'a', b'bc', b'asd'))