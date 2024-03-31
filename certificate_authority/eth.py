
from config import ChainConnection
from web3 import Web3

chain = ChainConnection()

def send_register(domain: str, pubkey: str):
    eth_chain = chain.eth_chain
    contract = chain.contract.eth_contract
    
    Chain_id = eth_chain.eth.chain_id
    nonce = eth_chain.eth.get_transaction_count(chain.admin.account_address)
    # Call your function
    call_function = contract.functions.register(domain, pubkey).build_transaction({"chainId": Chain_id, "from": chain.admin.account_address, "nonce": nonce})

    # Sign transaction
    signed_tx = eth_chain.eth.account.sign_transaction(call_function, private_key=chain.admin.account_key)

    # Send transaction
    send_tx = eth_chain.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for transaction receipt
    tx_receipt = eth_chain.eth.wait_for_transaction_receipt(send_tx)
    
    return (tx_receipt)

if __name__ == '__main__':
    res = send_register("test.com", "testpubkey")
    ls = chain.contract.eth_contract.functions.get(0).call()
    print(ls)