from cryptography.x509 import Certificate as X509Certificate

class SmartContractCertificate:
    def __init__(self) -> None:
        pass

class CertificateMapper:
    @staticmethod
    def to_x509(certificate: SmartContractCertificate) -> X509Certificate:
        raise NotImplementedError
    
    @staticmethod
    def from_x509(certificate: X509Certificate) -> SmartContractCertificate:
        raise NotImplementedError