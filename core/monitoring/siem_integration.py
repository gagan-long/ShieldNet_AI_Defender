from elasticsearch import Elasticsearch
from prometheus_api_client import PrometheusConnect
from typing import List, Dict
from loguru import logger
from datetime import datetime

class AISiem:
    def __init__(self, es_host: str = "http://localhost:9200"):
        self.es = Elasticsearch(es_host)
        self.prom = PrometheusConnect()
        self._setup_indices()

    def _setup_indices(self):
        """Initialize Elasticsearch mappings"""
        if not self.es.indices.exists(index="ai-security-logs"):
            self.es.indices.create(
                index="ai-security-logs",
                body={
                    "mappings": {
                        "properties": {
                            "timestamp": {"type": "date"},
                            "severity": {"type": "keyword"},
                            "model": {"type": "keyword"},
                            "message": {"type": "text"}
                        }
                    }
                }
            )

    def ingest_logs(self, logs: List[Dict]):
        """Bulk ingest security events"""
        actions = [
            {
                "_index": "ai-security-logs",
                "_source": {
                    **log,
                    "@timestamp": datetime.now().isoformat()
                }
            }
            for log in logs
        ]
        self.es.bulk(actions=actions)

    def detect_anomalies(self):
        """Run correlation queries"""
        query = """
        max_over_time(
            api_errors_total[5m]
        ) > 10
        and
        rate(
            model_drift_score[5m]
        ) > 0.8
        """
        results = self.prom.custom_query(query)
        
        if results:
            self._trigger_incident({
                "type": "anomaly_detected",
                "metrics": results[0]["value"]
            })

    def _trigger_incident(self, data: Dict):
        """Auto-remediation workflow"""
        from core.incident.response import AutoRemediator
        remediator = AutoRemediator()
        remediator.execute_playbook(data)

    def generate_report(self, days: int = 7) -> Dict:
        """Generate security posture report"""
        query = {
            "query": {
                "range": {
                    "@timestamp": {
                        "gte": f"now-{days}d/d"
                    }
                }
            },
            "aggs": {
                "threat_types": {
                    "terms": {"field": "severity"}
                },
                "model_activity": {
                    "terms": {"field": "model"}
                }
            }
        }
        return self.es.search(index="ai-security-logs", body=query)
