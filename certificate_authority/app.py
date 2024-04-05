import connexion
import config
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
    try:
        transaction = Transaction.from_json_string(transaction)
        result = registration_service.register_request(RegistrationRequest(transaction, ApprovalStatus.Pending))
        return result
    except Exception as e:
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )

def get_request(transaction: str):
    try:
        transaction = Transaction.from_json_string(transaction)
    except Exception as e:
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )
    try:
        result = registration_service.get_request(transaction)
    except:
        return connexion.problem(
            title = "NotFound",
            detail = "The requested resource was not found",
            status = 404,
        )
    headers = {"Content-Type": "application/json"}
    return result, 200, headers

def get_transaction(id: int):
    try:
        headers = {"Content-Type": "application/json"}
        return chain_service.get_transaction(id), 200, headers
    except:
        return connexion.problem(
            title = "NotFound",
            detail = "The requested resource was not found",
            status = 404,
        )

# admin
def get_all_requests():
    return registration_service.get_all_requests()

# admin
def get_pending_requests():
    return registration_service.get_pending_requests()

# admin
def approve_request(transaction: str):
    try:
        transaction = Transaction.from_json_string(transaction)
        result = registration_service.approve(transaction)
        return result
    except Exception as e:
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )

# admin
def reject_request(transaction: str):
    try:
        transaction = Transaction.from_json_string(transaction)
        result = registration_service.reject(transaction)
        return result
    except Exception as e:
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )
        

app = connexion.FlaskApp(__name__, swagger_ui_options=options, specification_dir="spec")
app.add_api('openapi.yaml')

if __name__ == '__main__':
    app.run(f"{Path(__file__).stem}:app", host=config.flask_host, port=8080)