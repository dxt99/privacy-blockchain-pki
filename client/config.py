import os

# Flask settings
flask_host = os.environ['host'] if 'host' in os.environ else '127.0.0.1'