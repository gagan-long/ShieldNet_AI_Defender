from elasticsearch import Elasticsearch
from prometheus_api_client import PrometheusConnect

class AISiem:
    def __init__(self):
        self.es = Elasticsearch(['https://elastic:9200'])
        self.prom = PrometheusConnect()
        
    def ingest_logs(self, logs):
        for log in logs:
            self.es.index(
                index="ai-security-logs",
                document={
                    "@timestamp": log.timestamp,
                    "message": log.message,
                    "severity": log.severity,
                    "model": log.model_id
                }
            )
    
    def run_ai_correlation(self):
        query = """
        avg_over_time(api_errors_total[5m]) > 10 
        AND 
        rate(model_drift_score[5m]) > 0.8
        """
        result = self.prom.custom_query(query)
        
        if result:
            self.trigger_incident(response.json())

    def trigger_incident(self, data):
        from core.incident.auto_responder import AIRemediator
        responder = AIRemediator()
        responder.handle_incident(data)
