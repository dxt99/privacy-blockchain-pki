from flask import Flask
from cryptography import x509

app = Flask(__name__)

@app.route("/")
def hello_world():
    builder = x509.CertificateSigningRequestBuilder()
    return "<p>Hello, World!</p>"

app.run("localhost", 8080)