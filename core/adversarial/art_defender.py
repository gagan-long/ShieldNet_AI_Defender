from art.estimators.classification import SklearnClassifier
from art.defences.trainer import AdversarialTrainer
from sklearn.ensemble import RandomForestClassifier

def train_robust_model(X, y):
    model = RandomForestClassifier(n_estimators=100)
    classifier = SklearnClassifier(model=model)
    
    # Generate adversarial examples
    from art.attacks.evasion import FastGradientMethod
    attack = FastGradientMethod(estimator=classifier, eps=0.2)
    
    # Adversarial training
    trainer = AdversarialTrainer(classifier, attacks=attack, ratio=0.5)
    trainer.fit(X, y)
    
    return classifier
