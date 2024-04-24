from chain_service import ChainService
from model import Transaction

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
    
if __name__ == '__main__':
    test_transactions_deserialization()
    
def test_chain_service():
    service = ChainService()
    res = service.is_revoked(2000000)
    assert(not res)
