import connexion
import config
import requests
from pathlib import Path
from connexion.options import SwaggerUIOptions


def verify():
    return "hello"

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
    app.run(f"{Path(__file__).stem}:app", host=config.flask_host, port=8100)