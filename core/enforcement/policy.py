from opa.client.opa_client import OPAClient
import grpc

class PolicyEnforcer:
    def __init__(self):
        self.channel = grpc.insecure_channel('opa:8181')
        self.client = OPAClient(self.channel)
        
    def check_access(self, user, resource, action):
        input_data = {
            "user": user,
            "resource": resource,
            "action": action,
            "time": datetime.now().isoformat()
        }
        
        result = self.client.check_policy(
            package="ai.security",
            rule="allow_access",
            input=input_data
        )
        
        if not result.result:
            self._log_violation(input_data)
            return False
            
        return True

    def _log_violation(self, input_data):
        from auditlog import AuditLogger
        AuditLogger.log(
            event="ACCESS_DENIED",
            data=input_data,
            severity="CRITICAL"
        )

# OPA Policy (ai-security.rego)
package ai.security

default allow_access = false

allow_access {
    input.user.roles[_] == "ai_operator"
    input.action == "infer"
    valid_model(input.resource)
}

valid_model(model) {
    startswith(model, "prod-")
}
