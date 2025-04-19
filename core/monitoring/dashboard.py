import gradio as gr
import numpy as np
from prometheus_client import start_http_server, Counter, Gauge
from typing import Dict, List
from loguru import logger
from datetime import datetime

# Prometheus Metrics
DETECTION_COUNTER = Counter(
    'adv_detections_total',
    'Total adversarial detections',
    ['attack_type']
)

CONFIDENCE_GAUGE = Gauge(
    'model_confidence',
    'Model prediction confidence',
    ['sample_id']
)

LATENCY_GAUGE = Gauge(
    'inference_latency_seconds',
    'Model inference latency'
)

class SecurityDashboard:
    def __init__(self, port: int = 9090):
        self.port = port
        self.detection_history = []
        self.start_time = datetime.now()
        
    def start_metrics_server(self):
        """Start Prometheus metrics endpoint"""
        start_http_server(self.port)
        logger.info(f"Metrics server started on port {self.port}")

    def log_detection(self, result: Dict):
        """Log detection event to history and metrics"""
        self.detection_history.append({
            **result,
            "timestamp": datetime.now().isoformat()
        })
        
        DETECTION_COUNTER.labels(
            attack_type=result.get("attack_type", "unknown")
        ).inc()
        
        CONFIDENCE_GAUGE.labels(
            sample_id=result.get("sample_id", "0")
        ).set(result["confidence"])

    def create_web_interface(self):
        """Create Gradio web interface"""
        with gr.Blocks(title="ShieldNet Dashboard") as interface:
            gr.Markdown("# 🔒 ShieldNet Security Dashboard")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("## 📈 Detection Metrics")
                    total_detections = gr.Label(label="Total Threats Blocked")
                    attack_distribution = gr.BarPlot(
                        x="attack_type",
                        y="count",
                        title="Attack Type Distribution"
                    )
                    
                with gr.Column():
                    gr.Markdown("## ⚠️ Recent Events")
                    event_log = gr.DataFrame(
                        headers=["Time", "Attack Type", "Confidence"],
                        datatype=["str", "str", "number"],
                        interactive=False
                    )
            
            interface.load(
                self._update_metrics,
                outputs=[total_detections, attack_distribution, event_log],
                every=5
            )
            
        return interface

    def _update_metrics(self):
        """Generate real-time metrics"""
        counts = {}
        for entry in self.detection_history:
            counts[entry["attack_type"]] = counts.get(entry["attack_type"], 0) + 1
            
        distribution_data = {
            "attack_type": list(counts.keys()),
            "count": list(counts.values())
        }
        
        recent_events = sorted(
            self.detection_history[-10:], 
            key=lambda x: x["timestamp"],
            reverse=True
        )
        
        event_data = [[
            e["timestamp"],
            e["attack_type"],
            f"{e['confidence']:.2f}"
        ] for e in recent_events]
        
        return (
            {"Total Threats Blocked": len(self.detection_history)},
            distribution_data,
            event_data
        )

    def run(self):
        """Start monitoring services"""
        self.start_metrics_server()
        interface = self.create_web_interface()
        interface.launch(server_port=7860, share=False)

# Quick Start Example
if __name__ == "__main__":
    dashboard = SecurityDashboard()
    
    # Simulate test events
    for _ in range(5):
        dashboard.log_detection({
            "attack_type": np.random.choice(["fgsm", "pgd", "clean"]),
            "confidence": np.random.uniform(0.7, 0.99),
            "sample_id": str(np.random.randint(1000))
        })
    
    dashboard.run()
