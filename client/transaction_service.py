import config
from key_manager import KeyManager
from ca_service import CaService
from model import Transaction
from typing import List

class TransactionService:
    name: str
    key_manager: KeyManager
    register_transaction: Transaction = None

    def __init__(self):
        self.name = config.client_common_name
        self.key_manager = KeyManager()
    
    @staticmethod
    def __serialize_signatures(*signatures: bytes):
        return f'({",".join([i.hex() for i in signatures])})'
    
    def generate_and_register(self) -> bool:
        self.register_transaction = None
        self.key_manager.new_key_chain()
        
        online_key = self.key_manager.online_keys[0]
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
    
    def register_request_status(self) -> str:
        if self.register_transaction == None:
            return "No transaction found"
        return CaService.transaction_status(self.register_transaction)
    
if __name__ == '__main__':
    print(TransactionService.__serialize_signatures(b'a', b'bc', b'asd'))