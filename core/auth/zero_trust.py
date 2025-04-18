import spacy
from datetime import datetime
from kubernetes import client, config

class ZeroTrustGatekeeper:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
        
    def validate_request(self, user: str, prompt: str, model: str):
        # Contextual analysis
        doc = self.nlp(prompt)
        if any(ent.label_ in ['PERSON', 'ORG'] for ent in doc.ents):
            return False
        
        # Behavioral analysis
        if self._check_anomalous_pattern(user):
            return False
            
        # Least privilege enforcement
        if not self._model_access_allowed(user, model):
            return False
            
        return True

    def _check_anomalous_pattern(self, user):
        # Query Prometheus for user behavior metrics
        from prometheus_api_client import PrometheusConnect
        prom = PrometheusConnect()
        query = f'''
        rate(
            api_requests_total{{user="{user}"}}[5m]
        ) > 100
        '''
        result = prom.custom_query(query)
        return bool(result)

    def _model_access_allowed(self, user, model):
        # Check Kubernetes RBAC
        auth_api = client.AuthorizationV1Api()
        review = client.V1SelfSubjectAccessReview(
            spec={
                "resourceAttributes": {
                    "group": "ai.shieldnet.io",
                    "resource": "models",
                    "verb": "use",
                    "name": model
                }
            }
        )
        return auth_api.create_self_subject_access_review(review).status.allowed

# Usage
zt = ZeroTrustGatekeeper()
if not zt.validate_request("alice", "Analyze patient records", "medical-llm"):
    print("Access denied by zero-trust policy")
