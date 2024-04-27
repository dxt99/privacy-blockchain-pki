import connexion
import config
import requests
from pathlib import Path
from model import Transaction
from connexion.options import SwaggerUIOptions
from transaction_service import TransactionService

service = TransactionService()

def hello():
    return "hello"

def register():
    try:
        service.generate_and_register()
    except Exception as e:
        return connexion.problem(
            title = "Bad request",
            detail = str(e),
            status = 400
        )
    
def get_transactions():
    return service.get_transactions()
    
def update(destination_key: bytes | dict):
    try:
        print(type(destination_key))
        if type(destination_key) == bytes: destination_key = destination_key.decode().strip()
        if type(destination_key) == dict: destination_key = ""
        return service.update_key(destination_key)
    except Exception as e:
        return connexion.problem(
            title = "Bad request",
            detail = str(e),
            status = 400
        )

def verify(transactions: dict):
    obj = Transaction.parse_transaction_list(transactions)
    return str(service.verify(obj))

def revoke():
    try:
        if service.revoke_key():
            return
        return connexion.problem(
            title = "Bad request",
            detail = "Failed to request key revocation",
            status = 400
        )
    except Exception as e:
        return connexion.problem(
            title = "Bad request",
            detail = str(e),
            status = 400
        )

def status():
    return service.register_request_status()

def ca_status(transaction: dict):
    url = f"{config.ca_base_url}/status"
    res = requests.post(url, json=transaction)
    try:
        payload = res.json()
        headers = {"Content-Type": "application/json"}
        return payload, 200, headers
    except:
        return connexion.problem(
            title = "Bad request",
            detail = res.text,
            status = res.status_code,
        )

options = SwaggerUIOptions(swagger_ui_path="/swagger")
app = connexion.FlaskApp(__name__, swagger_ui_options=options, specification_dir="spec")
app.add_api('openapi.yaml')

if __name__ == '__main__':
    app.run(f"{Path(__file__).stem}:app", host=config.flask_host, port=config.client_port)