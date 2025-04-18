import unittest
from core.adversarial.art_defender import train_robust_model
from sklearn.datasets import make_classification

class TestSecurity(unittest.TestCase):
    def test_art_training(self):
        X, y = make_classification(n_samples=1000, n_features=20)
        model = train_robust_model(X, y)
        self.assertIsNotNone(model.predict(X[0:1]))
