import connexion
import config
from pathlib import Path
from connexion.options import SwaggerUIOptions

options = SwaggerUIOptions(swagger_ui_path="/swagger")

def hello():
    return "hello"

def hello2():
    return "hi"

app = connexion.FlaskApp(__name__, swagger_ui_options=options, specification_dir="spec")
app.add_api('openapi.yaml')

if __name__ == '__main__':
    app.run(f"{Path(__file__).stem}:app", host=config.flask_host, port=8090)