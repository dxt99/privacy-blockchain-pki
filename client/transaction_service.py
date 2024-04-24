import config
from key_manager import KeyManager
from ca_service import CaService
from chain_service import ChainService
from model import Transaction
from typing import Dict
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

class TransactionService:
    chain_service: ChainService
    key_manager: KeyManager
    
    name: str
    register_transaction: Transaction = None
    register_transaction_id: int = -1
    update_transactions: Dict[int, Transaction]
    verifier_key: rsa.RSAPublicKey = None

    def __init__(self):
        self.name = config.client_common_name
        self.key_manager = KeyManager()
        self.chain_service = ChainService()
    
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
    
    def generate_and_register(self) -> bool:
        self.register_transaction = None
        self.key_manager.new_key_chain()
        
        online_key = self.key_manager.base_key
        master_key = self.key_manager.master_key
        online_signature: bytes = KeyManager.sign(online_key, self.name)
        master_signature: bytes = KeyManager.sign(master_key, self.name)
        signatures: str = self.__serialize_signatures(online_signature, master_signature)
        
        register_transaction = Transaction(
            identity = self.name,
            public_key = KeyManager.public_key_str(online_key),
            signatures = signatures
        )
        
        res = CaService.register_transaction(register_transaction)
        if res: self.register_transaction = register_transaction
        return res
    
    def update_key(self) -> bool:
        self.__get_verifier_key()
        if not self.register_transaction:
            print("Cannnot udpate key, no registration found")
            return False
        
        new_key = self.key_manager.add_key_to_chain()
        public_key = KeyManager.public_key_str(new_key)
        prev_data = self.register_transaction.public_key
        
        previous_signature: bytes = KeyManager.sign(new_key, prev_data)
        encrypted_signature: bytes = KeyManager.encrypt(self.verifier_key, previous_signature)
        online_signature: bytes = KeyManager.sign(new_key, public_key)
        
        signatures: str = self.__serialize_signatures(online_signature, encrypted_signature)
        update_transaction = Transaction(
            identity = "",
            public_key = public_key,
            signatures = signatures
        )
        id = self.chain_service.update(update_transaction)
        self.update_transactions[id] = update_transaction
        return True
    
    def register_request_status(self) -> str:
        if self.register_transaction == None:
            return "No transaction found"
        res, id = CaService.transaction_status(self.register_transaction)
        self.register_transaction_id = res
        return res
    
if __name__ == '__main__':
    print(TransactionService.__serialize_signatures(b'a', b'bc', b'asd'))