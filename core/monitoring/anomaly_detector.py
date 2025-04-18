# core/monitoring/anomaly_detector.py
from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.01)

    def train(self, normal_data):
        self.model.fit(normal_data)

    def detect(self, input_data):
        scores = self.model.decision_function(input_data)
        predictions = self.model.predict(input_data)
        return predictions, scores

# Usage
detector = AnomalyDetector()
detector.train(normal_traffic_data)
predictions, scores = detector.detect(new_data_points)
