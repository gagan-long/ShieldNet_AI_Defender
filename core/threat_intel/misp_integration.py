# core/threat_intel/misp_integration.py
from pymisp import ExpandedPyMISP
import json

class ThreatFeed:
    def __init__(self, config_path='configs/misp_credentials.json'):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.misp = ExpandedPyMISP(
            url=self.config['misp_url'],
            key=self.config['misp_key'],
            ssl=True
        )

    def get_ai_threats(self):
        return self.misp.search(
            tags=['ai_security', 'llm_exploit'],
            publish_timestamp='30d'
        )

# Usage
feed = ThreatFeed()
recent_threats = feed.get_ai_threats()
