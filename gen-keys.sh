openssl genpkey -out certificate_authority/config/key.pem -algorithm RSA -pkeyopt rsa_keygen_bits:4096
openssl genpkey -out verifier/config/verifier_key/key.pem -algorithm RSA -pkeyopt rsa_keygen_bits:4096
cp verifier/config/verifier_key/key.pem certificate_authority/config/verifier_key/key.pem