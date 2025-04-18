import unittest
from chaos_engineering import AIChaosMonkey
from core.attestation.verifier import AttestationVerifier
from core.crypto.quantum_safe import QuantumSafeEncryptor

class SecurityValidation(unittest.TestCase):
    def test_chaos_resilience(self):
        chaos = AIChaosMonkey()
        chaos.simulate_attack("prompt_injection")
        chaos.simulate_attack("model_poisoning")
        
    def test_attestation(self):
        verifier = AttestationVerifier()
        quote = get_quote_from_enclave()
        self.assertTrue(verifier.verify_quote(quote, nonce="test123"))
        
    def test_quantum_encryption(self):
        qc = QuantumSafeEncryptor()
        test_data = b"model_weights"
        encrypted = qc.encrypt_model(test_data)
        decrypted = qc.decrypt_model(encrypted)
        self.assertEqual(test_data, decrypted)

if __name__ == "__main__":
    unittest.main()
