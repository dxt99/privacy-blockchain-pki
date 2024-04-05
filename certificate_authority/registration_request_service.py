from typing import List
from model import RegistrationRequest, Transaction, ApprovalStatus
from repository import RegistrationRepository
from chain_service import ChainService

class RegistrationRequestService:
    def __init__(self):
        self.__repository = RegistrationRepository()
        self.__chain_service = ChainService()
    
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
        self.__repository.update_rqeuest(new_request)
        
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
        self.__repository.update_rqeuest(new_request)
        
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