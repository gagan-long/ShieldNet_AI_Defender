from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import kyber

class QuantumSafeEncryptor:
    def __init__(self):
        self.private_key, self.public_key = kyber.generate_keypair()
        
    def encrypt_model(self, model_bytes):
        ciphertext, shared_secret = kyber.enc(self.public_key)
        aes_key = hashes.Hash(hashes.SHA3_512())
        aes_key.update(shared_secret)
        final_key = aes_key.finalize()[:32]
        
        # Use AES-GCM with quantum-safe key
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        nonce = os.urandom(12)
        aesgcm = AESGCM(final_key)
        return nonce + aesgcm.encrypt(nonce, model_bytes, None)
    
    def decrypt_model(self, encrypted_data):
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        
        shared_secret = kyber.dec(self.private_key, ciphertext)
        aes_key = hashes.Hash(hashes.SHA3_512())
        aes_key.update(shared_secret)
        final_key = aes_key.finalize()[:32]
        
        aesgcm = AESGCM(final_key)
        return aesgcm.decrypt(nonce, ciphertext, None)
