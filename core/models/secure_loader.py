from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
import os

class ConfidentialModelLoader:
    def __init__(self):
        # Get key from SGX-protected memory
        self.key = self._get_protected_key()
        
    def _get_protected_key(self):
        # In real implementation, use SGX protected fs
        return os.environ['MODEL_ENCRYPTION_KEY'].encode()

    def load_model(self, path):
        with open(path, 'rb') as f:
            nonce = f.read(12)
            ciphertext = f.read()
        
        aesgcm = AESGCM(self.key)
        model_data = aesgcm.decrypt(nonce, ciphertext, None)
        
        # Verify integrity
        if not self._validate_checksum(model_data):
            raise SecurityException("Model tampering detected")
            
        return self._deserialize(model_data)

    def _validate_checksum(self, data):
        sha3 = hashlib.sha3_512()
        sha3.update(data)
        return sha3.digest() == data[-64:]

    def _deserialize(self, data):
        import tempfile
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(data[:-64])  # Remove checksum
            tmp.flush()
            return tf.keras.models.load_model(tmp.name)
