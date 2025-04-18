import tensorflow as tf
from tensorflow_privacy.privacy.optimizers.dp_optimizer import DPGradientDescentGaussianOptimizer

class DPTrainer:
    def __init__(self, l2_norm_clip=1.0, noise_multiplier=0.5, num_microbatches=8):
        self.optimizer = DPGradientDescentGaussianOptimizer(
            l2_norm_clip=l2_norm_clip,
            noise_multiplier=noise_multiplier,
            num_microbatches=num_microbatches,
            learning_rate=0.15
        )
        
    def train_model(self, model, dataset, epochs=3):
        loss_fn = tf.keras.losses.CategoricalCrossentropy(
            reduction=tf.losses.Reduction.NONE)
        
        model.compile(optimizer=self.optimizer, loss=loss_fn)
        return model.fit(dataset, epochs=epochs)
