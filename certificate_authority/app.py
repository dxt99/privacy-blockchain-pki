import connexion
import chain_service
from pathlib import Path
from model import RegisterTransaction
from connexion.options import SwaggerUIOptions
from cryptography.hazmat.primitives.asymmetric import rsa

options = SwaggerUIOptions(swagger_ui_path="/swagger")

def register_transaction_handler(transaction: str):
    register_transaction = RegisterTransaction.from_json_string(transaction)
    return { 'message': 'Success', 'your_name': register_transaction.identity }

def get_secret(user):
    return "hi"

app = connexion.FlaskApp(__name__, swagger_ui_options=options, specification_dir="spec")
app.add_api('openapi.yaml')

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

if __name__ == '__main__':
    app.run(f"{Path(__file__).stem}:app", port=8080)