from typing import List
from model import RegistrationRequest, Transaction
from repository import RegistrationRepository
from chain_service import ChainService

class RegistrationRequestService:
    def __init__(self):
        self.__repository = RegistrationRepository()
        self.__chain_service = ChainService()
    
    def register_request(self, request: RegistrationRequest) -> str:
        pending_requests = self.__repository.get_pending_requests()
        if any([request.transaction.identity == pending_request.transaction.identity for pending_request in pending_requests]):
            raise Exception("One request at a time")
        self.__repository.register_request(request)
        return "Success"
    
    def approve(self, transaction: Transaction):
        pending_requests = self.__repository.get_pending_requests()
        target_requests = [request for request in pending_requests if request.transaction.identity == transaction.identity]
        if len(target_requests) != 1:
            raise Exception(f"There seems to be {len(target_requests)} pending request for this identity, this should not be possible")
        target_request = target_requests[0]
        if target_request.transaction.public_key != transaction.public_key:
            raise Exception(f"Public key stored in the database is different.")
        self.__repository.approve(target_request)
        self.__chain_service.register(transaction)
        return "Success"
    
    def get_pending_requests(self) -> List[RegistrationRequest]:
        return self.__repository.get_pending_requests()
    
    def get_all_requests(self) -> List[RegistrationRequest]:
        return self.__repository.get_requests()