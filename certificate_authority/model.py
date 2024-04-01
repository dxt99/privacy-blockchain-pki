import datetime
import json
from dataclasses import dataclass
from cryptography import x509
from cryptography.x509 import Certificate as X509Certificate
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization import Encoding

one_day = datetime.timedelta(1, 0, 0)

@dataclass
class Transaction:
    identity: str
    public_key: str
    
    @staticmethod
    def from_json_string(transaction_json):
        identity = transaction_json["identity"]
        public_key = transaction_json["public_key"]
        return Transaction(identity, public_key)
        

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