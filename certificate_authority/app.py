import connexion
import config
from pathlib import Path
from typing import List
from model import Transaction, RegistrationRequest, ApprovalStatus, RegistrationRequestDto
from chain_service import ChainService
from registration_request_service import RegistrationRequestService
from revocation_request_service import RevocationRequestService
from validate_service import ValidateService
from x509_service import X509Service
from connexion.options import SwaggerUIOptions

options = SwaggerUIOptions(swagger_ui_path="/swagger")
chain_service = ChainService()
registration_service = RegistrationRequestService()
revocation_service = RevocationRequestService()
validation_service = ValidateService()
x509_service = X509Service()

def register_transaction(transaction: dict):
    try:
        transaction = Transaction.from_json_string(transaction)
        if not validation_service.validate(transaction):
            return connexion.problem(
                title = "BadOperation",
                detail = "Transaction is invalid. Make sure that identity is present, public key is generated correctly, and siganture is signed properly",
                status = 400,
            )
        result = registration_service.register_request(RegistrationRequest(transaction, ApprovalStatus.Pending))
        return result
    except Exception as e:
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )

def get_request(transaction: dict):
    try:
        transaction = Transaction.from_json_string(transaction)
        if not validation_service.validate(transaction):
            return connexion.problem(
                title = "BadOperation",
                detail = "Transaction is invalid. Make sure that identity is present, public key is generated correctly, and siganture is signed properly",
                status = 400,
            )
    except Exception as e:
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )
    try:
        result = registration_service.get_request(transaction)
        result = RegistrationRequestDto.fromModel(result)
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
        
def revoke_request(transaction: dict):
    try:
        transaction = Transaction.from_json_string(transaction)
        if not validation_service.validate(transaction):
            return connexion.problem(
                title = "BadOperation",
                detail = "Transaction is invalid. Make sure that identity is present, public key is generated correctly, and siganture is signed properly",
                status = 400,
            )
        return revocation_service.issue_challenge(transaction)
    except Exception as e:
        print(e)
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )

def revoke_challenge(challenge: dict):
    try:
        transaction = Transaction.from_json_string(challenge["transaction"])
        if not validation_service.validate(transaction):
            return connexion.problem(
                title = "BadOperation",
                detail = "Transaction is invalid. Make sure that identity is present, public key is generated correctly, and siganture is signed properly",
                status = 400,
            )
        signature = bytes.fromhex(challenge["challenge_signature"])
        if revocation_service.try_challenge(transaction, signature):
            x509_service.revoke_timestamp(transaction)
            return "Success"
        else:
            return "Failed"
    except Exception as e:
        print(e)
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )
        
def x509_serialize(transaction: dict):
    try:
        transaction = Transaction.from_json_string(transaction)
        if not validation_service.validate(transaction):
            return connexion.problem(
                title = "BadOperation",
                detail = "Transaction is invalid. Make sure that identity is present, public key is generated correctly, and siganture is signed properly",
                status = 400,
            )
        result = x509_service.get_x509cert(transaction)
        return result.decode()
    except Exception as e:
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )
        
def x509_crl():
    result = x509_service.get_crl()
    return result.decode()

# admin
def get_all_requests():
    return list(map(RegistrationRequestDto.fromModel, registration_service.get_all_requests()))

# admin
def get_pending_requests():
    return list(map(RegistrationRequestDto.fromModel, registration_service.get_pending_requests()))

# admin
def get_revocation_requests():
    return list(map(RegistrationRequestDto.fromModel, revocation_service.get_revoke_requests()))

# admin
def approve_request(transaction: dict):
    try:
        transaction = Transaction.from_json_string(transaction)
        if not validation_service.validate(transaction):
            return connexion.problem(
                title = "BadOperation",
                detail = "Transaction is invalid. Make sure that identity is present, public key is generated correctly, and siganture is signed properly",
                status = 400,
            )
        result = registration_service.approve(transaction)
        return result
    except Exception as e:
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )

# admin
def reject_request(transaction: dict):
    try:
        transaction = Transaction.from_json_string(transaction)
        if not validation_service.validate(transaction):
            return connexion.problem(
                title = "BadOperation",
                detail = "Transaction is invalid. Make sure that identity is present, public key is generated correctly, and siganture is signed properly",
                status = 400,
            )
        result = registration_service.reject(transaction)
        return result
    except Exception as e:
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )
        
# admin
def revoke_transaction(transaction: dict):
    try:
        transaction = Transaction.from_json_string(transaction)
        if not validation_service.validate(transaction):
            return connexion.problem(
                title = "BadOperation",
                detail = "Transaction is invalid. Make sure that identity is present, public key is generated correctly, and siganture is signed properly",
                status = 400,
            )
        result = registration_service.revoke(transaction)
        return result
    except Exception as e:
        print(e)
        return connexion.problem(
            title = "BadOperation",
            detail = str(e),
            status = 400,
        )
        
app = connexion.FlaskApp(__name__, swagger_ui_options=options, specification_dir="spec")
app.add_api('openapi.yaml')

if __name__ == '__main__':
    registration_service.initialize()
    app.run(f"{Path(__file__).stem}:app", host=config.flask_host, port=8080)