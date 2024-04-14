import os

# Flask settings
flask_host = os.environ['host'] if 'host' in os.environ else '127.0.0.1'
ca_base_url = os.environ['ca_url'] if 'ca_url' in os.environ else 'http://localhost:8080'