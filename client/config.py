import os


# Flask settings
flask_host = os.environ['host'] if 'host' in os.environ else '127.0.0.1'
ca_base_url = os.environ['ca_url'] if 'ca_url' in os.environ else 'http://localhost:8080'
client_port = int(os.environ['port']) if 'port' in os.environ else 8090

# Certificate settings
client_common_name = os.environ['common_name'] if 'common_name' in os.environ else f"client{client_port}.com"