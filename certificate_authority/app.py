import connexion
from pathlib import Path
from model import Transaction
from chain_service import ChainService
from connexion.options import SwaggerUIOptions

options = SwaggerUIOptions(swagger_ui_path="/swagger")
chain_service = ChainService()

def register_transaction(transaction: str):
    register_transaction = Transaction.from_json_string(transaction)
    # TODO: check if ongoing application is already present in database
    return 'Success'

def get_transaction(id: int):
    try:
        return chain_service.get_transaction(id)
    except:
        return connexion.problem(
            title="NotFound",
            detail="The requested resource was not found",
            status=404,
        )

app = connexion.FlaskApp(__name__, swagger_ui_options=options, specification_dir="spec")
app.add_api('openapi.yaml')

if __name__ == '__main__':
    app.run(f"{Path(__file__).stem}:app", port=8080)