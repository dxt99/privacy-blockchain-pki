import os
import json
from web3 import Web3
from dataclasses import dataclass

# Flask settings
flask_host = os.environ['host'] if 'host' in os.environ else '127.0.0.1'
ca_base_url = os.environ['ca_url'] if 'ca_url' in os.environ else 'http://localhost:8080'
client_port = int(os.environ['port']) if 'port' in os.environ else 8090

# Certificate settings
client_common_name = os.environ['common_name'] if 'common_name' in os.environ else f"client{client_port}.com"
verifier_tx_id = 0

# CA smart contract
@dataclass
class SmartContract:
    ca_abi: str
    ca_address: str
    eth_contract: any
    
    def __init__(self, chain: Web3):
        buffer = open("config/contracts/PrivCA.json").read()
        ca_json = json.loads(buffer)
        self.ca_abi = ca_json["abi"]
        self.ca_address = ca_json["networks"]["5777"]["address"]
        self.eth_contract = chain.eth.contract(address=self.ca_address, abi=self.ca_abi)
        

# CA smart contract account
@dataclass
class ClientAccount:
    account_address: str
    account_key: str
    
    def __init__(self):
        buffer = open("config/account.json").read()
        account_json = json.loads(buffer)
        self.account_address = account_json["address"]
        self.account_key = account_json["key"]

# Web3 chain connection
@dataclass
class ChainConnection:
    client: ClientAccount
    eth_chain: Web3
    contract: SmartContract
    
    def __init__(self):
        eth_address = os.environ['chain_url'] if 'chain_url' in os.environ else 'http://127.0.0.1:7545'
        self.client = ClientAccount()
        self.eth_chain = Web3(Web3.HTTPProvider(eth_address))
        assert(self.eth_chain.is_connected())
        self.contract = SmartContract(self.eth_chain)
        