import os
from typing import Dict, List
from datetime import datetime, timezone
from model import Transaction, ApprovalStatus, RegistrationRequest
from repository import RegistrationRepository
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class RevocationRequestService:
    challenges: Dict[str, bytes]
    
    def __init__(self):
        self.__repository = RegistrationRepository()
        self.challenges = {}
        
    def issue_challenge(self, transaction: Transaction) -> str:
        results = self.__repository.get_request(transaction)
        if len(results) != 1:
            raise Exception(f"Transaction not found")
        request: RegistrationRequest = results[0]
        status = request.status
        if status != ApprovalStatus.Approved:
            raise Exception(f"Transaction is in {status.value}, expected status is {ApprovalStatus.Approved.value}")
        challenge = os.urandom(64)
        self.challenges[transaction.public_key] = challenge
        return challenge.hex()
        
    def try_challenge(self, transaction: Transaction, signature: bytes) -> bool:
        results = self.__repository.get_request(transaction)
        if len(results) != 1:
            raise Exception(f"Transaction not found")
        request: RegistrationRequest = results[0]
        status = request.status
        if status != ApprovalStatus.Approved:
            raise Exception(f"Transaction is in {status.value}, expected status is {ApprovalStatus.Approved.value}")
        challenge = self.challenges[transaction.public_key]
        
        pub_key = serialization.load_pem_public_key(bytes.fromhex(transaction.public_key))
        try:
            pub_key.verify(signature, challenge, 
                        algorithm=hashes.SHA256(),
                        padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH))
            request.status = ApprovalStatus.RevocationRequested
            self.__repository.update_rqeuest(request)
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_revoke_requests(self) -> List[RegistrationRequest]:
        return self.__repository.get_revocation_request()