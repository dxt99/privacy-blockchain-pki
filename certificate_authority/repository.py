import sqlite3
from config import sqlite_db_file
from model import RegistrationRequest, Transaction, ApprovalStatus
from typing import List

class RegistrationRepository:
    def __init__(self):
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS registrations(identity, public_key, signatures, approval_status, id)")
        conn.commit()
        
    def __rows_to_registration_requests(self, rows):
        return [RegistrationRequest(Transaction(row[0], row[1], row[2]), ApprovalStatus[row[3]], int(row[4])) for row in rows]
    
    def __get_connection(self):
        try:
            conn = sqlite3.connect(sqlite_db_file)
            return conn
        except Exception as e:
            print("Failed to get sqlite db connection")
            
    def update_request(self, request: RegistrationRequest):
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute(f"UPDATE registrations set approval_status = '{request.status.value}', id = '{request.id}' WHERE identity = ? AND public_key = ? AND signatures = ?",
                    (request.transaction.identity, request.transaction.public_key, request.transaction.signatures))
        conn.commit()
    
    def get_requests(self) -> List[RegistrationRequest]:
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute(f"SELECT * FROM registrations").fetchall()
        return self.__rows_to_registration_requests(res)
    
    def get_pending_requests(self) -> List[RegistrationRequest]:
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute(f"SELECT * FROM registrations WHERE approval_status = '{ApprovalStatus.Pending.value}'").fetchall()
        return self.__rows_to_registration_requests(res)
    
    def get_revocation_request(self) -> List[RegistrationRequest]:
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute(f"SELECT * FROM registrations WHERE approval_status = '{ApprovalStatus.RevocationRequested.value}'").fetchall()
        return self.__rows_to_registration_requests(res)
    
    def get_revoked(self) -> List[RegistrationRequest]:
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute(f"SELECT * FROM registrations WHERE approval_status = '{ApprovalStatus.Revoked.value}'").fetchall()
        return self.__rows_to_registration_requests(res)
    
    def register_request(self, request: RegistrationRequest):
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO registrations VALUES (?, ?, ?, ?, ?)", 
                    (request.transaction.identity, request.transaction.public_key, request.transaction.signatures, request.status.value, str(request.id)))
        conn.commit()
        
    def get_request(self, transaction: Transaction) -> List[RegistrationRequest]:
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute(f"SELECT * FROM registrations WHERE identity = ? AND public_key = ? AND signatures = ?",
                    (transaction.identity, transaction.public_key, transaction.signatures)).fetchall()
        return self.__rows_to_registration_requests(res)

    
if  __name__ == '__main__':
    repo = RegistrationRepository()
    request = RegistrationRequest(Transaction("test", "key", "hello"), ApprovalStatus.Pending)
    repo.register_request(request)
    print(repo.get_requests())