from Cryptodome.Random import random

class KeyManager:
    online_master_key: int
    offline_master_key: int
    
    def __init__(self):
        pass
    
    def new_key(self):
        random.getrandbits(512)