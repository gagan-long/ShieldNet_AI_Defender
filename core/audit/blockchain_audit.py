from web3 import Web3
import json

class BlockchainAuditor:
    def __init__(self, rpc_url):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        with open('contracts/ShieldNetAudit.json') as f:
            contract_abi = json.load(f)
        self.contract = self.w3.eth.contract(
            address='0xYourContractAddress',
            abi=contract_abi
        )
    
    def log_incident(self, event_hash, metadata):
        tx_hash = self.contract.functions.logIncident(
            event_hash,
            json.dumps(metadata)
        ).transact({'from': self.w3.eth.accounts[0]})
        
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)
    
    def verify_integrity(self, model_hash):
        return self.contract.functions.verifyModel(
            model_hash
        ).call()
