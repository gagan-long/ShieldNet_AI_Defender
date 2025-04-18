import requests
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives import hashes

class AttestationVerifier:
    IAS_URL = "https://api.trustedservices.intel.com/sgx/dev/attestation/v4/report"
    
    def verify_quote(self, quote, nonce):
        cert = load_pem_x509_certificate(open('ias_cert.pem', 'rb').read())
        cert.public_key().verify(
            quote.signature,
            quote.report_body,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        
        response = requests.post(
            self.IAS_URL,
            json={
                "isvEnclaveQuote": quote.b64_encoded,
                "nonce": nonce
            },
            headers={"Ocp-Apim-Subscription-Key": os.getenv('IAS_KEY')}
        )
        
        return response.json()['isvEnclaveQuoteBody']['status'] == "OK"

# Usage
verifier = AttestationVerifier()
if not verifier.verify_quote(quote, nonce):
    raise SecurityException("Enclave attestation failed")
