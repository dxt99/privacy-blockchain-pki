
from config import ChainConnection
from model import Transaction

class ChainService:
    def __init__(self):
        self.__chain = ChainConnection()
    
    def get_transaction(self, id: int) -> Transaction:
        _, identity, public_key, signatures = self.__chain.contract.eth_contract.functions.get(id).call()
        return Transaction(identity, public_key, signatures)
    
    def is_revoked(self, id: int) -> bool:
        return self.__chain.contract.eth_contract.functions.isRevoked(id).call()

if __name__ == '__main__':
    service = ChainService()
    #ls = service.register(Transaction("s", "a", "b"))
    print(service.is_revoked(0))