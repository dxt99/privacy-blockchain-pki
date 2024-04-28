import config
from typing import List
from model import RegistrationRequest, Transaction, ApprovalStatus
from repository import RegistrationRepository
from chain_service import ChainService
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class RegistrationRequestService:
    initialized = False
    
    def __init__(self):
        self.__repository = RegistrationRepository()
        self.__chain_service = ChainService()
    
    def initialize(self):
        # registering verifier to smart contract
        if RegistrationRequestService.initialized: return
        
        RegistrationRequestService.initialized = True
        pub_key = config.verifier_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1).hex()
        signature = config.verifier_key.sign(
            bytes.fromhex(pub_key), 
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
            )
        verifier_tx = Transaction(identity="verifier_service", public_key=pub_key, signatures=f"({signature.hex()})")
        request = RegistrationRequest(transaction=verifier_tx, status=ApprovalStatus.Pending)
        self.register_request(request)
        self.approve(verifier_tx)
    
    def register_request(self, new_request: RegistrationRequest) -> str:
        all_requests = self.__repository.get_requests()
        if any([new_request.transaction.identity == request.transaction.identity and request.status == ApprovalStatus.Pending for request in all_requests]):
            raise Exception("One request at a time")
        if any([new_request.transaction == request.transaction for request in all_requests]):
            raise Exception("Cannot reregister the same transaction")
        self.__repository.register_request(new_request)
        return "Success"
    
    def approve(self, transaction: Transaction):
        pending_requests = self.__repository.get_pending_requests()
        target_requests = [request for request in pending_requests if request.transaction.identity == transaction.identity]
        if len(target_requests) != 1:
            raise Exception(f"There seems to be {len(target_requests)} pending request for this identity, this should not be possible")
        target_request = target_requests[0]
        if target_request.transaction.public_key != transaction.public_key:
            raise Exception(f"Public key stored in the database is different.")
        if target_request.transaction.signatures != transaction.signatures:
            raise Exception(f"Signatures stored in the database is different.")
        new_id = self.__chain_service.register(transaction)
        new_request = RegistrationRequest(transaction, ApprovalStatus.Approved, new_id)
        self.__repository.update_request(new_request)
        
        return "Success"
    
    def reject(self, transaction: Transaction):
        pending_requests = self.__repository.get_pending_requests()
        target_requests = [request for request in pending_requests if request.transaction.identity == transaction.identity]
        if len(target_requests) != 1:
            raise Exception(f"There seems to be {len(target_requests)} pending request for this identity, this should not be possible")
        target_request = target_requests[0]
        if target_request.transaction.public_key != transaction.public_key:
            raise Exception(f"Public key stored in the database is different.")
        if target_request.transaction.signatures != transaction.signatures:
            raise Exception(f"Signatures stored in the database is different.")
        new_request = RegistrationRequest(transaction, ApprovalStatus.Rejected, -1)
        self.__repository.update_request(new_request)
        
        return "Success"
    
    def revoke(self, transaction: Transaction):
        results = self.__repository.get_request(transaction)
        if len(results) != 1:
            raise Exception(f"Transaction not found")
        target_request = results[0]
        new_request = RegistrationRequest(transaction, ApprovalStatus.Revoked, target_request.id)
        self.__chain_service.revoke(target_request.id)
        self.__repository.update_request(new_request)
        
        return "Success"
    
    def get_request(self, transaction: Transaction) -> RegistrationRequest:
        results = self.__repository.get_request(transaction)
        if len(results) != 1:
            raise Exception(f"Transaction not found")
        return results[0]
    
    def get_pending_requests(self) -> List[RegistrationRequest]:
        return self.__repository.get_pending_requests()
    
    def get_all_requests(self) -> List[RegistrationRequest]:
        return self.__repository.get_requests()