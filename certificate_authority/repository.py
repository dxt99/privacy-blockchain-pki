import sqlite3
from config import sqlite_db_file
from model import RegistrationRequest, Transaction, ApprovalStatus
from typing import List

class RegistrationRepository:
    def __init__(self):
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS registrations(identity, public_key, approval_status)")
        conn.commit()
    
    def __get_connection(self):
        try:
            conn = sqlite3.connect(sqlite_db_file)
            return conn
        except Exception as e:
            print("Failed to get sqlite db connection")
            
    def approve(self, request: RegistrationRequest):
        raise NotImplementedError
    
    def reject(self, request: RegistrationRequest):
        raise NotImplementedError
    
    def get_requests(self) -> List[RegistrationRequest]:
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute(f"SELECT * FROM registrations").fetchall()
        requests = [RegistrationRequest(Transaction(row[0], row[1]), row[2]) for row in res]
        return requests
    
    def get_pending_requests(self) -> List[RegistrationRequest]:
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute(f"SELECT * FROM registrations WHERE approval_status = '{ApprovalStatus.Pending.value}'").fetchall()
        requests = [RegistrationRequest(Transaction(row[0], row[1]), row[2]) for row in res]
        return requests
    
    def register_request(self, request: RegistrationRequest):
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO registrations VALUES (?, ?, ?)", 
                    (request.transaction.identity, request.transaction.public_key, request.status.value))
        conn.commit()

    
if  __name__ == '__main__':
    repo = RegistrationRepository()
    request = RegistrationRequest(Transaction("test", "key"), ApprovalStatus.Pending)
    repo.register_request(request)
    print(repo.get_requests())