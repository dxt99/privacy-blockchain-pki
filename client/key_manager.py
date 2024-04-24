from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from typing import List

class KeyManager:
    public_key_exponent: int = 0x10001
    key_size: int = 2048
    master_key: rsa.RSAPrivateKey
    online_keys: List[rsa.RSAPrivateKey]
    offline_keys: List[rsa.RSAPublicKey]
    
    def __init__(self):
        pass
    
    def __gen_generic_key(self):
        return rsa.generate_private_key(self.public_key_exponent,  self.key_size)
    
    @staticmethod
    def public_key_str(key: rsa.RSAPrivateKey):
        return key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1).hex()
    
    @staticmethod
    def sign(key: rsa.RSAPrivateKey, payload: bytes | str) -> bytes:
        encoded_payload = payload if type(payload) == bytes else payload.encode()
        return key.sign(
            encoded_payload, 
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
            )
    
    def new_key_chain(self):
        self.master_key = self.__gen_generic_key()
        self.online_keys = [self.__gen_generic_key()]
        self.offline_keys = [self.__gen_generic_key()]
        
    def add_key_to_chain(self):
        raise NotImplementedError
        
if __name__ == '__main__':
    key = rsa.generate_private_key(0x10001, 2048)
    print(key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption()))
    print(key.public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.PKCS1))
    #print(KeyManager.sign(key, b"data"))