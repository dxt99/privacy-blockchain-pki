from chain_service import ChainService
from model import Transaction

def test_chain_service():
    service = ChainService()
    res = service.is_revoked(2000000)
    assert(not res)
    
def test_transaction_serialization():
    service = Transaction(
        identity="name",
        public_key="0x12abcdef",
        signatures="0xabcdef12"
    )
    obj = service.to_dict()
    assert(obj["identity"] == "name")