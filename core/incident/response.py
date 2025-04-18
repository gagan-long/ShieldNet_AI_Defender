# core/incident/response.py
import smtplib
from datetime import datetime

class IncidentResponder:
    def __init__(self):
        self.log_file = "incidents.log"
        
    def log_incident(self, event):
        with open(self.log_file, 'a') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"{timestamp} - {event}\n")
        
        self.alert_team(event)

    def alert_team(self, event):
        # Send email alert
        msg = f"Subject: Security Incident\n\n{event}"
        
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login('alert@yourdomain.com', 'password')
            server.sendmail(
                'alert@yourdomain.com', 
                'security-team@yourdomain.com', 
                msg
            )

# Usage
responder = IncidentResponder()
responder.log_incident("Detected prompt injection attempt")
