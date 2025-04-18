# core/adversarial/tester.py
from art.attacks.evasion import FastGradientMethod
import tensorflow as tf

class ModelTester:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.classifier = TensorFlowV2Classifier(self.model)

    def run_attack(self, x_test, y_test):
        attack = FastGradientMethod(estimator=self.classifier, eps=0.1)
        x_test_adv = attack.generate(x=x_test)
        
        # Evaluate accuracy
        predictions = self.model.predict(x_test_adv)
        accuracy = tf.reduce_mean(
            tf.cast(tf.equal(tf.argmax(predictions, 1), y_test), tf.float32)
        )
        
        return accuracy.numpy()

# Usage
tester = ModelTester('./models/sentiment_analysis.h5')
accuracy = tester.run_attack(x_test, y_test)
print(f"Model accuracy under attack: {accuracy:.2%}")
