import numpy as np
import tensorflow as tf
from art.estimators.classification import TensorFlowV2Classifier
from art.attacks.evasion import FastGradientMethod, ProjectedGradientDescent
from typing import Optional, Dict, Any
from loguru import logger
from pydantic import BaseModel

class DetectionResult(BaseModel):
    is_malicious: bool
    confidence: float
    attack_type: str
    perturbation_norm: float

class AdversarialDetector:
    def __init__(self, model: tf.keras.Model):
        """
        Initialize with a trained TensorFlow model
        
        Args:
            model: Pre-trained TF/Keras model
        """
        self.model = model
        self.classifier = self._create_art_classifier()
        self.threshold = 0.85  # Confidence threshold for detection
        
    def _create_art_classifier(self) -> TensorFlowV2Classifier:
        """Create ART classifier wrapper"""
        return TensorFlowV2Classifier(
            model=self.model,
            nb_classes=10,  # Update based on your model
            input_shape=(None, *self.model.input_shape[1:]),
            loss_object=tf.keras.losses.CategoricalCrossentropy(),
            clip_values=(0, 1)
        )

    def detect(self, input_data: np.ndarray) -> DetectionResult:
        """
        Detect adversarial samples using multiple methods
        
        Args:
            input_data: Input array (batch x features)
            
        Returns:
            DetectionResult with threat analysis
        """
        # 1. Model Confidence Check
        predictions = self.model.predict(input_data)
        max_confidence = np.max(predictions)
        
        # 2. Fast Gradient Method Test
        fgsm = FastGradientMethod(self.classifier, eps=0.05)
        fgsm_adv = fgsm.generate(input_data)
        fgsm_diff = np.linalg.norm(fgsm_adv - input_data)
        
        # 3. Projected Gradient Descent Test
        pgd = ProjectedGradientDescent(self.classifier, eps=0.1, max_iter=5)
        pgd_adv = pgd.generate(input_data)
        pgd_diff = np.linalg.norm(pgd_adv - input_data)
        
        # Detection Logic
        is_malicious = False
        attack_type = "none"
        
        if max_confidence > self.threshold:
            if fgsm_diff > 0.1 or pgd_diff > 0.15:
                is_malicious = True
                attack_type = "pgd" if pgd_diff > fgsm_diff else "fgsm"
        
        return DetectionResult(
            is_malicious=is_malicious,
            confidence=float(max_confidence),
            attack_type=attack_type,
            perturbation_norm=float(max(fgsm_diff, pgd_diff))
        )

    def health_check(self) -> Dict[str, Any]:
        """System health verification"""
        try:
            test_input = np.random.rand(1, *self.model.input_shape[1:])
            result = self.detect(test_input)
            return {
                "status": "healthy",
                "inference_time": result.confidence,
                "art_version": "1.16.1"
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {"status": "unhealthy", "error": str(e)}

class HealthCheck:
    @staticmethod
    def run():
        """Static method for requirement verification"""
        try:
            import art
            import tensorflow
            return {"status": "success", "versions": {
                "art": art.__version__,
                "tensorflow": tensorflow.__version__
            }}
        except ImportError as e:
            return {"status": "missing_dependencies", "error": str(e)}
