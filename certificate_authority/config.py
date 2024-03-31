import json
from web3 import Web3

# DB file
sqlite_db_file = "db/certtificate_authority.db"

# CA smart contract
class SmartContract:
    def __init__(self, chain: Web3):
        buffer = open("config/contracts/PrivCA.json").read()
        ca_json = json.loads(buffer)
        self.ca_abi = ca_json["abi"]
        self.ca_address = ca_json["networks"]["5777"]["address"]
        self.eth_contract = chain.eth.contract(address=self.ca_address, abi=self.ca_abi)
        

# CA smart contract account
class AdminAccount:
    def __init__(self):
        buffer = open("config/account.json").read()
        account_json = json.loads(buffer)
        self.account_address = account_json["address"]
        self.account_key = account_json["key"]

# Web3 chain connection
class ChainConnection:
    def __init__(self):
        eth_address = 'http://127.0.0.1:7545'
        self.admin = AdminAccount()
        self.eth_chain = Web3(Web3.HTTPProvider(eth_address))
        assert(self.chain.is_connected())
        self.contract = SmartContract(self.eth_chain)
        

if __name__ == "__main__":
    chain = ChainConnection()
    print(chain.contract.ca_abi)
    print(chain.contract.ca_address)