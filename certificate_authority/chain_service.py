
from config import ChainConnection

class ChainService:
    def __init__(self):
        self.__chain = ChainConnection()

    def register(self, domain: str, pubkey: str) -> str:
        eth_chain = self.__chain.eth_chain
        contract = self.__chain.contract.eth_contract
        
        Chain_id = eth_chain.eth.chain_id
        nonce = eth_chain.eth.get_transaction_count(self.__chain.admin.account_address)
        # Call your function
        call_function = contract.functions.register(domain, pubkey).build_transaction({"chainId": Chain_id, "from": self.__chain.admin.account_address, "nonce": nonce})

        # Sign transaction
        signed_tx = eth_chain.eth.account.sign_transaction(call_function, private_key=self.__chain.admin.account_key)

        # Send transaction
        send_tx = eth_chain.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Wait for transaction receipt
        tx_receipt = eth_chain.eth.wait_for_transaction_receipt(send_tx)
        
        return (tx_receipt)
    
    def get_transaction(self, id: int) -> str:
        return self.__chain.contract.eth_contract.functions.get(0).call()

if __name__ == '__main__':
    service = ChainService()
    res = service.send_register("test.com", "testpubkey")
    ls = service.get_transaction(0)
    print(ls)