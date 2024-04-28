import config
import datetime
from typing import Dict
from model import Transaction, ApprovalStatus
from repository import RegistrationRepository
from cryptography import x509
from cryptography.x509 import Certificate as X509Certificate, RevokedCertificateBuilder, CertificateRevocationListBuilder
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509.oid import NameOID

class X509Service:
    def __init__(self):
        self.__repository = RegistrationRepository()
        self.certs: Dict[int, X509Certificate] = {}
        self.revokes: Dict[int, datetime.datetime] = {}
        
    def get_x509cert(self, transaction: Transaction) -> bytes:
        results = self.__repository.get_request(transaction)
        if len(results) != 1:
            raise Exception(f"Transaction not found")
        request = results[0]
        if request.status != ApprovalStatus.Approved:
            raise Exception(f"Transaction is in {request.status.value} status, not in approved status")
        
        if request.id in self.certs:
            return CertificateMapper.x509_to_bytes(self.certs[request.id])
        
        cert = CertificateMapper.to_x509(transaction, request.id)
        self.certs[request.id] = cert
        return CertificateMapper.x509_to_bytes(cert)
    
    def revoke_timestamp(self, transaction: Transaction):
        results = self.__repository.get_request(transaction)
        if len(results) != 1:
            raise Exception(f"Transaction not found in x509")
        request = results[0]
        self.revokes[request.id] = datetime.datetime.now()
    
    def get_crl(self) -> bytes:
        revoked = self.__repository.get_revoked()
        builder = x509.CertificateRevocationListBuilder()
        builder = builder.last_update(datetime.datetime.today())
        builder = builder.next_update(datetime.datetime.today() + one_day)
        builder = builder.issuer_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, 'certificate_authority'),
        ]))
        for request in revoked:
            if request.id in self.certs:
                revoked_cert = x509.RevokedCertificateBuilder().serial_number(request.id + CertificateMapper.base_id).revocation_date(self.revokes[request.id]).build()
                builder = builder.add_revoked_certificate(revoked_cert)
        crl = builder.sign(private_key=config.private_key, algorithm=hashes.SHA256())
        return crl.public_bytes(serialization.Encoding.PEM)


one_day = datetime.timedelta(1, 0, 0)

class CertificateMapper:
    base_id = 90000
    
    @staticmethod
    def to_x509(tx: Transaction, id: int) -> X509Certificate:
        private_key = config.private_key
        builder = x509.CertificateBuilder()
        builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, tx.identity),
        ]))
        builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, 'certificate_authority'),
        ]))
        builder = builder.not_valid_before(datetime.datetime.today() - one_day)
        builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 30))
        builder = builder.serial_number(id + CertificateMapper.base_id)
        key = serialization.load_pem_public_key(bytes.fromhex(tx.public_key))
        builder = builder.public_key(key)
        builder = builder.add_extension(
            x509.SubjectAlternativeName(
                [x509.DNSName('certificate_authority')]
            ),
            critical=False
        )
        builder = builder.add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True,
        )
        signature = tx.signature_parse()[0]
        builder = builder.add_extension(
            x509.SubjectKeyIdentifier(signature), critical= True
        )
        certificate = builder.sign(
            private_key=private_key, algorithm=hashes.SHA256(),
        )
        return certificate
    
    @staticmethod
    def x509_to_bytes(certificate: X509Certificate) -> bytes:
        return certificate.public_bytes(encoding=serialization.Encoding.PEM)
    
    @staticmethod
    def bytes_to_x509(payload: bytes) -> X509Certificate:
        return x509.load_pem_x509_certificate(payload)
    
    @staticmethod
    def from_x509(certificate: X509Certificate) -> Transaction:
        identity = certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        pub_key = certificate.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1).hex()
        signature = certificate.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value.digest.hex()
        return Transaction(identity, pub_key, signature)