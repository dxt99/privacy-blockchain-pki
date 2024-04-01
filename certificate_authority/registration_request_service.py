from model import RegistrationRequest
from repository import RegistrationRepository

class RegistrationRequestService:
    def __init__(self):
        self.__repository = RegistrationRepository()
    
    def register_request(self, request: RegistrationRequest):
        pending_requests = self.__repository.get_pending_requests()
        if any([request.transaction.identity == pending_request.transaction.identity for pending_request in pending_requests]):
            return "Failed"
        self.__repository.register_request(request)
        return "Success"
    
    def get_pending_requests(self):
        return self.__repository.get_pending_requests()
    
    def get_all_requests(self):
        return self.__repository.get_requests()