from typing import Optional, List
from kubernetes import client, config
import spacy
from loguru import logger
from prometheus_api_client import PrometheusConnect
from pydantic import BaseModel

class AccessRequest(BaseModel):
    user: str
    prompt: str
    model: str
    session_id: str

class ZeroTrustGatekeeper:
    def __init__(self, prometheus_url: str = "http://localhost:9090"):
        self.nlp = spacy.load("en_core_web_lg")
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.prom = PrometheusConnect(url=prometheus_url)
        
    def validate_request(self, request: AccessRequest) -> bool:
        """Enhanced validation with session tracking"""
        checks = [
            self._check_prompt_safety(request.prompt),
            self._check_behavioral_anomaly(request.user),
            self._check_model_access(request.user, request.model),
            self._verify_session(request.session_id)
        ]
        return all(checks)

    def _check_prompt_safety(self, prompt: str) -> bool:
        """Advanced NLP-based injection detection"""
        doc = self.nlp(prompt)
        danger_patterns = {
            'PERSON': ['credentials', 'password', 'token'],
            'ORG': ['database', 'system', 'config']
        }
        
        for ent in doc.ents:
            if ent.label_ in danger_patterns:
                for pattern in danger_patterns[ent.label_]:
                    if pattern in ent.text.lower():
                        logger.warning(f"Blocked harmful pattern: {ent.text}")
                        return False
        return True

    def _check_behavioral_anomaly(self, user: str) -> bool:
        """Real-time Prometheus metrics check"""
        query = f'''
        rate(
            api_requests_total{{user="{user}"}}[5m]
        ) > 100
        and
        avg_over_time(
            response_size_bytes{{user="{user}"}}[5m]
        ) > 1e6
        '''
        try:
            result = self.prom.custom_query(query)
            return len(result) == 0
        except Exception as e:
            logger.error(f"Prometheus query failed: {e}")
            return False

    def _check_model_access(self, user: str, model: str) -> bool:
        """Kubernetes RBAC-style verification"""
        auth_api = client.AuthorizationV1Api()
        review = auth_api.create_self_subject_access_review(
            body={
                "spec": {
                    "resourceAttributes": {
                        "namespace": "models",
                        "verb": "use",
                        "resource": "ai-models",
                        "name": model
                    }
                }
            }
        )
        return review.status.allowed

    def _verify_session(self, session_id: str) -> bool:
        """Session integrity check"""
        # Implement JWT or OAuth2 verification here
        return True if session_id.startswith("secure-") else False
