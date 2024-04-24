from chain_service import ChainService
from model import Transaction
from cryptography.hazmat.primitives import serialization

def test_transactions_deserialization():
    service = Transaction(
        identity="name",
        public_key="0x12abcdef",
        signatures="0xabcdef12"
    )
    item = {
        "0": service.to_dict(),
        "1": service.to_dict()
    }
    obj = Transaction.parse_transaction_list(item)
    assert(obj[0] == service)
    
def test_transaction_signature_deserialization():
    tx = Transaction(
        identity="name",
        public_key="0x12abcdef",
        signatures="(abcdef12,abefefef)"
    )
    signatures = tx.signature_parse()
    assert(signatures[0] == bytes.fromhex('abcdef12'))
    assert(signatures[1] == bytes.fromhex('abefefef'))
    
def test_chain_service():
    service = ChainService()
    res = service.is_revoked(2000000)
    assert(not res)
