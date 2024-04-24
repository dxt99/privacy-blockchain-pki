openssl genpkey -out verifier/config/verifier_key/key.pem -algorithm RSA -pkeyopt rsa_keygen_bits:2048
cp verifier/config/verifier_key/key.pem certificate_authority/config/verifier_key/key.pem