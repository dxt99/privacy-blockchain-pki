
from config import ChainConnection
from model import Transaction

class ChainService:
    def __init__(self):
        self.__chain = ChainConnection()

    def register(self, transaction: Transaction) -> str:
        eth_chain = self.__chain.eth_chain
        contract = self.__chain.contract.eth_contract
        
        Chain_id = eth_chain.eth.chain_id
        nonce = eth_chain.eth.get_transaction_count(self.__chain.admin.account_address)
        # Call your function
        call_function = contract.functions.register(transaction.identity, transaction.public_key, transaction.signatures).build_transaction({"chainId": Chain_id, "from": self.__chain.admin.account_address, "nonce": nonce})
        
        # Get return value
        res = contract.functions.register(transaction.identity, transaction.public_key, transaction.signatures).call({"from": self.__chain.admin.account_address})
    
        # Sign transaction
        signed_tx = eth_chain.eth.account.sign_transaction(call_function, private_key=self.__chain.admin.account_key)

        # Send transaction
        send_tx = eth_chain.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Wait for transaction receipt
        eth_chain.eth.wait_for_transaction_receipt(send_tx)
        
        return res
    
    def revoke(self, transaction_id: int) -> bool:
        eth_chain = self.__chain.eth_chain
        contract = self.__chain.contract.eth_contract
        
        Chain_id = eth_chain.eth.chain_id
        nonce = eth_chain.eth.get_transaction_count(self.__chain.admin.account_address)
        
        # Call your function
        call_function = contract.functions.revoke((transaction_id)).build_transaction({"chainId": Chain_id, "from": self.__chain.admin.account_address, "nonce": nonce})
        
        # Get return value
        res = contract.functions.revoke(transaction_id).call({"chainId": Chain_id, "from": self.__chain.admin.account_address})
    
        # Sign transaction
        signed_tx = eth_chain.eth.account.sign_transaction(call_function, private_key=self.__chain.admin.account_key)

        # Send transaction
        send_tx = eth_chain.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Wait for transaction receipt
        eth_chain.eth.wait_for_transaction_receipt(send_tx)
        
        return res
    
    def get_transaction(self, id: int) -> Transaction:
        identity, public_key, signatures = self.__chain.contract.eth_contract.functions.get(id).call()
        return Transaction(identity, public_key, signatures)
    
    def is_revoked(self, id: int) -> bool:
        return self.__chain.contract.eth_contract.functions.isRevoked(id).call()

if __name__ == '__main__':
    service = ChainService()
    #ls = service.register(Transaction("s", "a", "b"))
    ls = service.revoke(0)
    print(ls)
    print(service.is_revoked(0))