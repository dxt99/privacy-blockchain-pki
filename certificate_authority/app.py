import connexion
from pathlib import Path
from typing import List
from model import Transaction, RegistrationRequest, ApprovalStatus
from chain_service import ChainService
from registration_request_service import RegistrationRequestService
from connexion.options import SwaggerUIOptions

options = SwaggerUIOptions(swagger_ui_path="/swagger")
chain_service = ChainService()
registration_service = RegistrationRequestService()

def register_transaction(transaction: str):
    transaction = Transaction.from_json_string(transaction)
    result = registration_service.register_request(RegistrationRequest(transaction, ApprovalStatus.Pending))
    return result

def get_transaction(id: int):
    try:
        return chain_service.get_transaction(id)
    except:
        return connexion.problem(
            title="NotFound",
            detail="The requested resource was not found",
            status=404,
        )
        
def get_all_requests():
    return registration_service.get_all_requests()

app = connexion.FlaskApp(__name__, swagger_ui_options=options, specification_dir="spec")
app.add_api('openapi.yaml')

if __name__ == '__main__':
    app.run(f"{Path(__file__).stem}:app", port=8080)