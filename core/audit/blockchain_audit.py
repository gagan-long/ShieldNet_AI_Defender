from web3 import Web3, HTTPProvider
from eth_account import Account
from typing import Dict, Any
import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes

class BlockchainAuditor:
    def __init__(self, rpc_url: str, contract_address: str):
        self.w3 = Web3(HTTPProvider(rpc_url))
        with open('contracts/ShieldNetAudit.json') as f:
            self.contract_abi = json.load(f)
        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=self.contract_abi
        )
        self.account = Account.from_key('YOUR_PRIVATE_KEY')

    def log_incident(self, event_type: str, metadata: Dict[str, Any]) -> str:
        """Immutable log entry with cryptographic proof"""
        event_hash = self._generate_hash(metadata)
        
        tx = self.contract.functions.logIncident(
            event_type,
            event_hash,
            json.dumps(metadata)
        ).build_transaction({
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 2000000
        })
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def _generate_hash(self, data: Dict) -> str:
        """Generate SHA3-256 hash of metadata"""
        digest = hashes.Hash(hashes.SHA3_256())
        digest.update(json.dumps(data).encode())
        return digest.finalize().hex()

    def verify_entry(self, tx_hash: str) -> bool:
        """Verify blockchain entry integrity"""
        receipt = self.w3.eth.get_transaction_receipt(tx_hash)
        logs = self.contract.events.IncidentLogged().process_receipt(receipt)
        return len(logs) > 0
