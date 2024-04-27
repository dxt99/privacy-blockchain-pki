from dataclasses import dataclass
from enum import Enum
from typing import List

@dataclass
class Transaction:
    identity: str
    public_key: str
    signatures: str
    
    def signature_parse(self) -> List[bytes]:
        signature_strs = self.signatures.lstrip("(").rstrip(")").split(",")
        return list(map(bytes.fromhex, signature_strs))
    
    @staticmethod
    def from_json_string(transaction_json):
        identity = transaction_json["identity"]
        public_key = transaction_json["public_key"]
        signatures = transaction_json["signatures"]
        return Transaction(identity, public_key, signatures)

class ApprovalStatus(Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"
    RevocationRequested = "RevocationRequested"
    Revoked = "Revoked"
    
@dataclass
class RegistrationRequest:
    transaction: Transaction
    status: ApprovalStatus
    id: int = -1

@dataclass
class RegistrationRequestDto:
    transaction: Transaction
    status: str
    id: int = -1
    
    @staticmethod
    def fromModel(request: RegistrationRequest):
        return RegistrationRequestDto(
            request.transaction,
            request.status.value,
            request.id
        )

@dataclass
class SmartContractCertificate:
    def __init__(self) -> None:
        pass
    
if __name__ == '__main__':
    t1 = Transaction("a", "b", "c")
    t2 = Transaction("a", "b", "c")
    print(t1 == t2)