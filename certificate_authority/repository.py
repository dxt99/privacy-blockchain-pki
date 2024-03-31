import sqlite3
from config import sqlite_db_file
from model import SmartContractCertificate
from typing import List

class CertificateRepository:
    def __init__(self):
        conn = self.__get_connection()
        pass
    
    def __get_connection(self):
        try:
            conn = sqlite3.connect(sqlite_db_file)
            return conn
        except Exception as e:
            print("Failed to get sqlite db connection")
            
    def approve(self, certificate: SmartContractCertificate):
        raise NotImplementedError
    
    def reject(self, certificate: SmartContractCertificate):
        raise NotImplementedError
    
    def get_certificates(self) -> List[SmartContractCertificate]:
        raise NotImplementedError
    
    def register_requests(self, certificate: SmartContractCertificate):
        raise NotImplementedError
    
if  __name__ == '__main__':
    repo = CertificateRepository()