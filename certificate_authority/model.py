import datetime
from dataclasses import dataclass
from enum import Enum
from typing import List
from cryptography import x509
from cryptography.x509 import Certificate as X509Certificate
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

one_day = datetime.timedelta(1, 0, 0)

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

class CertificateMapper:
    @staticmethod
    def to_x509(certificate: SmartContractCertificate, private_key: rsa.RSAPrivateKey) -> X509Certificate:
        public_key = private_key.public_key()
        builder = x509.CertificateBuilder()
        builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, 'cryptography.io'),
        ]))
        builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, 'cryptography.io'),
        ]))
        builder = builder.not_valid_before(datetime.datetime.today() - one_day)
        builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 30))
        builder = builder.serial_number(x509.random_serial_number())
        builder = builder.public_key(public_key)
        builder = builder.add_extension(
            x509.SubjectAlternativeName(
                [x509.DNSName('cryptography.io')]
            ),
            critical=False
        )
        builder = builder.add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True,
        )
        certificate = builder.sign(
            private_key=private_key, algorithm=hashes.SHA256(),
        )
        return certificate
    
    @staticmethod
    def from_x509(certificate: X509Certificate) -> SmartContractCertificate:
        raise NotImplementedError
    
if __name__ == '__main__':
    t1 = Transaction("a", "b", "c")
    t2 = Transaction("a", "b", "c")
    print(t1 == t2)