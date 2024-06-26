from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from typing import List

class KeyManager:
    public_key_exponent: int = 0x10001
    key_size: int = 2048
    base_key: rsa.RSAPrivateKey
    online_keys: List[rsa.RSAPrivateKey]
    
    def __init__(self):
        self.base_key = None
        self.online_keys = []
    
    def __gen_generic_key(self, is_small = False):
        return rsa.generate_private_key(self.public_key_exponent,  self.key_size // (2 if is_small else 1))
    
    @staticmethod
    def public_key_str(key: rsa.RSAPrivateKey):
        return key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1).hex()
    
    @staticmethod
    def encrypt(key: rsa.RSAPublicKey, payload: bytes | str) -> bytes:
        encoded_payload = payload if type(payload) == bytes else payload.encode()
        
        return key.encrypt(
            encoded_payload, 
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    @staticmethod
    def sign(key: rsa.RSAPrivateKey, payload: bytes | str) -> bytes:
        encoded_payload = payload if type(payload) == bytes else payload.encode()
        return key.sign(
            encoded_payload, 
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
            )
    
    def new_key_chain(self):
        self.base_key = self.__gen_generic_key()
        self.online_keys = []
        
    def add_key_to_chain(self):
        new_key = self.__gen_generic_key(is_small=True)
        self.online_keys.append(new_key)
        return new_key
        
if __name__ == '__main__':
    key = rsa.generate_private_key(0x10001, 2048)
    print(key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption()))
    print(key.public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.PKCS1))