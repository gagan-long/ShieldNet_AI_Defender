import tensorflow as tf
from tensorflow_privacy.privacy.optimizers.dp_optimizer import DPGradientDescentGaussianOptimizer
from tensorflow_privacy.privacy.analysis import compute_dp_sgd_privacy
from typing import Tuple, Dict

class DPTrainer:
    def __init__(self, l2_norm_clip: float = 1.0, noise_multiplier: float = 0.5, 
                 num_microbatches: int = 8, learning_rate: float = 0.15):
        self.l2_norm_clip = l2_norm_clip
        self.noise_multiplier = noise_multiplier
        self.num_microbatches = num_microbatches
        self.learning_rate = learning_rate
        
    def train_model(self, model: tf.keras.Model, dataset: tf.data.Dataset, 
                   epochs: int = 3) -> Tuple[tf.keras.Model, Dict]:
        """
        Train with differential privacy
        
        Returns:
            model: Trained model
            privacy_report: DP guarantees
        """
        optimizer = DPGradientDescentGaussianOptimizer(
            l2_norm_clip=self.l2_norm_clip,
            noise_multiplier=self.noise_multiplier,
            num_microbatches=self.num_microbatches,
            learning_rate=self.learning_rate
        )
        
        loss_fn = tf.keras.losses.CategoricalCrossentropy(
            reduction=tf.losses.Reduction.NONE)
        
        model.compile(optimizer=optimizer, loss=loss_fn)
        history = model.fit(dataset, epochs=epochs)
        
        # Calculate DP guarantees
        privacy_report = self._calculate_privacy(
            len(dataset), 
            epochs=epochs
        )
        
        return model, privacy_report

    def _calculate_privacy(self, num_samples: int, 
                          epochs: int) -> Dict[str, float]:
        """Compute formal DP guarantees"""
        delta = 1e-5
        epsilon, _ = compute_dp_sgd_privacy(
            n=num_samples,
            batch_size=self.num_microbatches,
            noise_multiplier=self.noise_multiplier,
            epochs=epochs,
            delta=delta
        )
        return {
            "epsilon": epsilon,
            "delta": delta,
            "effective_noise": self.noise_multiplier * self.l2_norm_clip
        }
